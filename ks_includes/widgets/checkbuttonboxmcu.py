import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
class CheckButtonBoxMcu(Gtk.Box):
    def __init__(self, this, _content, onCheck=None, funVal=None, InitVal=None):
        super().__init__()
        self.onCheck = onCheck
        self.funVal = funVal
        self.button1 = Gtk.CheckButton(label=_content,name ="check-button-label")
        self.button1.connect("toggled", self.on_button_toggled)
        if(InitVal is not None):
             self.button1.set_active(InitVal)
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        info.set_halign(Gtk.Align.START)
        info.pack_start(self.button1, False, False, 0)
        self.add(info)

    def set_active(self, value):
        if self.button1.get_active() != value:
         self.button1.set_active(value)

    def on_button_toggled(self, button):
        if(self.onCheck is not None):
            if(self.funVal is not None):
                self.onCheck(button.get_active(), self.funVal)
            else:
                self.onCheck(button.get_active())
        if button.get_active():
            print("Radio butonu seçildi:", button.get_label())