import time
from datetime import datetime
import re
import gi
from ks_includes.widgets.bottommenu import BottomMenu
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ks_includes.screen_panel import ScreenPanel

COLORS = {
    "command": "#bad8ff",
    "error": "#ff6975",
    "response": "#b8b8b8",
    "time": "grey",
    "warning": "#c9c9c9"
}
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.menu = BottomMenu(self, False)
        self.autoscroll = True
        o1_lbl = Gtk.Label(_("Auto Scroll"))
        o1_switch = Gtk.CheckButton()
        o1_switch.set_active(self.autoscroll)
        o1_switch.connect("notify::active", self.set_autoscroll)
        if self._screen.vertical_mode:
            o1_lbl.set_halign(Gtk.Align.CENTER)
        else:
            o1_lbl.set_halign(Gtk.Align.END)
        refreshIcon = self._gtk.Image("update", self._screen.width *.02, self._screen.width *.02)
        o3_button = Gtk.Button(_("Clear"), name ="refresh-button")
        o3_button.connect("clicked", self.clear)
        o3_button.set_image(refreshIcon)
        o3_button.set_always_show_image(True)
        options = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        options.set_hexpand(True)
        options.pack_start(o1_switch, False, False, 0)
        options.pack_start(o1_lbl, False, False, 5)
        options.pack_end(o3_button, False, False, 0)

        sw = Gtk.ScrolledWindow()
        sw.set_hexpand(True)
        sw.set_vexpand(True)

        tb = Gtk.TextBuffer()
        tv = Gtk.TextView()
        tv.set_buffer(tb)
        tv.set_editable(False)
        tv.set_cursor_visible(False)
        tv.connect("size-allocate", self._autoscroll)
        tv.connect("focus-in-event", self._screen.remove_keyboard)
        tv.connect("focus-in-event", self.add_menu)

        sw.add(tv)

        ebox = Gtk.Box()
        ebox.set_hexpand(True)
        ebox.set_vexpand(False)

        entry = Gtk.Entry()
        entry.set_hexpand(True)
        entry.set_vexpand(False)
        entry.connect("button-press-event", self._screen.show_keyboard)
        entry.connect("button-press-event", self.hide_menu)
        entry.connect("focus-in-event", self._screen.show_keyboard)
        entry.connect("activate", self._send_command)
        entry.grab_focus_without_selecting()

        enter = Gtk.Button(_('Send'),name ="send-button")
        enter.set_hexpand(False)
        enter.connect("clicked", self._send_command)

        ebox.add(entry)
        ebox.add(enter)

        self.labels.update({
            "entry": entry,
            "sw": sw,
            "tb": tb,
            "tv": tv
        })

        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.content_box.add(sw)
        self.content_box.pack_start(options, False, False, 5)
        self.content_box.pack_start(ebox, False, False, 0)
        self.content_box.pack_end(self.menu, False, False, 0)
        
        self.content.add(self.content_box)

    def hide_menu(self, *args):
        self.content_box.remove(self.menu)
        
    def add_menu(self, *args):
        self.content_box.pack_end(self.menu, False, False, 0)
        
    def clear(self, widget=None):
        self.labels['tb'].set_text("")

    def add_gcode(self, msgtype, msgtime, message):
        if msgtype == "command":
            color = COLORS['command']
        elif message.startswith("!!"):
            color = COLORS['error']
            message = message.replace("!! ", "")
        elif message.startswith("//"):
            color = COLORS['warning']
            message = message.replace("// ", "")
        elif self.hidetemps and re.match('^(?:ok\\s+)?(B|C|T\\d*):', message):
            return
        else:
            color = COLORS['response']
        message = f'<span color="{color}"><b>{message}</b></span>'
        message = message.replace('\n', '\n         ')
        self.labels['tb'].insert_markup(
            self.labels['tb'].get_end_iter(),
            f'\n<span color="{COLORS["time"]}">{datetime.fromtimestamp(msgtime).strftime("%H:%M:%S")}</span> {message}',
            -1
        )
        # Limit the length
        if self.labels['tb'].get_line_count() > 999:
            self.labels['tb'].delete(self.labels['tb'].get_iter_at_line(0), self.labels['tb'].get_iter_at_line(1))

    def gcode_response(self, result, method, params):
        if method != "server.gcode_store":
            return

        for resp in result['result']['gcode_store']:
            self.add_gcode(resp['type'], resp['time'], resp['message'])

    def process_update(self, action, data):
        if action == "notify_gcode_response":
            self.add_gcode("response", time.time(), data)

    def set_autoscroll(self, *args):
        self.autoscroll ^= True

    def _autoscroll(self, *args):
        if self.autoscroll:
            adj = self.labels['sw'].get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size())

    def _send_command(self, *args):
        cmd = self.labels['entry'].get_text()
        self.labels['entry'].set_text('')
        self._screen.remove_keyboard()
        self.add_menu()
        self.add_gcode("command", time.time(), cmd)
        self._screen._ws.klippy.gcode_script(cmd)

    def activate(self):
        self.clear()
        self._screen._ws.send_method("server.gcode_store", {"count": 100}, self.gcode_response)