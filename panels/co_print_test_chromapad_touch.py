from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title) 
        self.test = set()
        self.autoOneButton = Gtk.Button('1',name ="touch-test-buttons")
        self.autoOneButton.connect("clicked", self.on_touch, 1)
        self.autoTwoButton = Gtk.Button('2',name ="touch-test-buttons")
        self.autoTwoButton.connect("clicked", self.on_touch, 2)
        self.autoThreeButton = Gtk.Button('3',name ="touch-test-buttons")
        self.autoThreeButton.connect("clicked", self.on_touch, 3)
        self.autoFourButton = Gtk.Button('4',name ="touch-test-buttons")
        self.autoFourButton.connect("clicked", self.on_touch, 4) 
        self.autoFiveButton = Gtk.Button('5',name ="touch-test-buttons")
        self.autoFiveButton.connect("clicked", self.on_touch, 5)
        fixed = Gtk.Fixed()
        fixed.set_valign(Gtk.Align.START)
        fixed.set_halign(Gtk.Align.START)
        fixed.put(self.autoOneButton, 5, 5)
        fixed.put(self.autoTwoButton, 5, 490)
        fixed.put(self.autoThreeButton, 935, 490)
        fixed.put(self.autoFourButton, 935, 5)
        fixed.put(self.autoFiveButton, 470, 250)
        fixedBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        fixedBox.pack_start(fixed, True, True, 0)
        self.content.add(fixedBox)

    def on_touch(self, widget, value):
        self.test.add(value)
        if len(self.test) == 5:
            self.test = set()
            self._screen.show_panel("co_print_test_chromapad_usb", "co_print_test_chromapad_usb ", "Language", 1, True)
            