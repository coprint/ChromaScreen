import gi
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.macros import Macros
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        menu = BottomMenu(self, False)
        macroLabel = Gtk.Label(_("Predefined Macros"), name="macro-label")
        macro_flowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        macro_flowbox.set_hexpand(True)
        self.scroll = self._gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_kinetic_scrolling(True)
        self.scroll.get_overlay_scrolling()
        self.scroll.set_vexpand(True)
        self.scroll.add(macro_flowbox)
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
        main.set_vexpand(True)
        main.set_hexpand(True)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(macroLabel, False, False, 0)
        main.pack_start(self.scroll, True, True, 0)
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(main, True, True, 0)
        page.pack_end(menu, False, True, 0)
        
        self.content.add(page)
        self.load_gcode_macros()

    def run_gcode_macro(self, widget, macro):
        params = ""
        self._screen._ws.klippy.gcode_script(f"{macro} {params}")

    def load_gcode_macros(self):
        self.macro_flowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.macro_flowbox.set_hexpand(True)
        for macro in self._printer.get_gcode_macros():
            macro = macro[12:].strip()
            if macro.startswith("_"):  # Support for hiding macros by name
                continue
            macroone = Macros(self, macro)
            self.macro_flowbox.pack_start(macroone, True, True, 0)
        for child in self.scroll.get_children():
            self.scroll.remove(child)
        self.scroll.add(self.macro_flowbox)
        self.content.show_all()