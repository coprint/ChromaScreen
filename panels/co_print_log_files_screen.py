import logging
import os
import time
from datetime import datetime
import re
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.infodialog import InfoDialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintLogFilesScreen(*args)

COLORS = {
    "command": "#bad8ff",
    "error": "#ff6975",
    "response": "#b8b8b8",
    "time": "grey",
    "warning": "#c9c9c9"
}
class CoPrintLogFilesScreen(ScreenPanel):


    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.menu = BottomMenu(self, False)
        self.title = title
        self.autoscroll = True

        
        

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
        ebox.set_halign(Gtk.Align.END)
        ebox.set_hexpand(True)
        ebox.set_vexpand(False)

        
        export = Gtk.Button(_('Back'),name ="send-button")
        export.set_hexpand(False)
        export.connect("clicked", self._send_command)

        
        ebox.add(export)

        self.labels.update({

            "sw": sw,
            "tb": tb,
            "tv": tv
        })

        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_box.pack_start(ebox, False, False, 0)
        self.content_box.add(sw)
        self.content_box.pack_end(self.menu, False, False, 0)
        self.content.add(self.content_box)

        self.timeout_id = GLib.timeout_add(1000, self.on_timeout, None)
        self.waitDialog = InfoDialog(self, _("Please Wait"), True)
        self.waitDialog.get_style_context().add_class("alert-info-dialog")
        self.waitDialog.set_decorated(False)
        self.waitDialog.set_size_request(0, 0)


        response = self.waitDialog.run()





    def on_timeout(self, *args, **kwargs):
        f = open(self._screen.log_path + "/" +  self.title, "r")
        file_content = f.read()
        for line in file_content.split("\n"):
            self.add_gcode("command", line)

        self.waitDialog.response(Gtk.ResponseType.CANCEL)
        self.waitDialog.destroy()
        self.timeout_id = None
        # self.destroy()
        return False

    def hide_menu(self, *args):
        self.content_box.remove(self.menu)
        
    def add_menu(self, *args):
        self.content_box.pack_end(self.menu, False, False, 0)
        
    def clear(self, widget=None):
        self.labels['tb'].set_text("")

    def add_gcode(self, msgtype, message):
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
            f'\n{message}',
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

    # def hide_temps(self, *args):
    #     self.hidetemps ^= True

    def set_autoscroll(self, *args):
        self.autoscroll ^= True

    def _autoscroll(self, *args):
        if self.autoscroll:
            adj = self.labels['sw'].get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size())

    def _send_command(self, *args):
        self._screen.show_panel("co_print_home_not_connected_screen", "co_print_home_not_connected_screen", "Language",
                                1, False)

    