import subprocess
import gi

from ks_includes.widgets.keyboard import Keyboard
from ks_includes.widgets.keyboarddialog import KeyboardDialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk


class ChangeMCUDialog(Gtk.Dialog):
    def __init__(self,name, this, defaultVal):
        super().__init__(title="My Dialog",parent=None ,flags=0)
        self.psw = None
        self.this = this
        self.ssid = this
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.set_default_size(300, 100)
        pos = self.get_position()
        self.move(pos[0] + 345, pos[1] + 100)
        title = Gtk.Label(name, name="add-network-dialog-title")
        self.SSIDentry = Gtk.Entry(name="network-input")
        self.SSIDentry.set_placeholder_text(_("Wifi SSID"))
        self.SSIDentry.connect("touch-event", self.give_name, self.SSIDentry)
    

        eventBox = Gtk.EventBox()
        eventBox.connect("button-press-event", self.give_name, self.SSIDentry)
        eventBox.add(self.SSIDentry)


        self.passwordEntry = Gtk.Entry(name="network-input")
        self.passwordEntry.set_placeholder_text(_("Value"))
        self.passwordEntry.connect("touch-event", self.give_name, self.passwordEntry    )
        self.passwordEntry.set_text(defaultVal)

        eventBoxPsw = Gtk.EventBox()
        eventBoxPsw.connect("button-press-event", self.give_name, self.passwordEntry)
        eventBoxPsw.add(self.passwordEntry)

        box = self.get_content_area()
        box.set_spacing(20)
        box.set_name("info-dialog-content-box")
        box.add(title)
        #box.add(eventBox)
        box.add(eventBoxPsw)
        self.show_all()
    
    def give_name(self,a,b,entryName):
       
        self.dialog = KeyboardDialog(self.this._screen, self.remove_keyboard, entry=entryName)
        self.dialog.get_style_context().add_class("keyboard-dialog")
       
        self.dialog.set_decorated(False)

        response = self.dialog.run()
 
        if response == Gtk.ResponseType.OK:
            self.dialog.destroy()
            psw = self.passwordEntry.get_text()
            ssid = self.SSIDentry.get_text()
            command = ["nmcli", "device", "wifi", "connect", ssid, "password", psw]
            self.execute_command_and_show_output(command, ssid, psw)
            
        elif response == Gtk.ResponseType.CANCEL:
            self.dialog.destroy()

    def remove_keyboard(self, widget=None, event=None):
         self.psw = self.passwordEntry.get_text()
         self.ssid = self.SSIDentry.get_text()
         self.dialog.destroy()
  