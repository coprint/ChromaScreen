import subprocess
import gi
import numpy as np

from ks_includes.widgets.keyboard import Keyboard
from ks_includes.widgets.keyboarddialog import KeyboardDialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk


class AreYouSureDialog(Gtk.Dialog):
    def __init__(self,name, this):
        super().__init__(title="My Dialog",parent=None ,flags=0)

       
       
        self.this = this
        self.ssid = name
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.set_default_size(300, 100)
        pos = self.get_position()
        self.move(pos[0] + 345, pos[1] + 100)
        title = Gtk.Label(_("Are you sure?"), name="add-network-dialog-title")
        self.SSIDentry = Gtk.Entry(name="network-input")
        self.SSIDentry.set_placeholder_text(_("Wifi SSID"))
        self.SSIDentry.connect("touch-event", self.give_name, self.SSIDentry)


        eventBox = Gtk.EventBox()
        eventBox.connect("button-press-event", self.give_name, self.SSIDentry)
        eventBox.add(self.SSIDentry)


        if name != '':
            self.SSIDentry.set_text(name)
            self.SSIDentry.set_editable(False)
            self.SSIDentry.set_can_focus(False)





        self.passwordEntry = Gtk.Entry(name="network-input")
        self.passwordEntry.set_placeholder_text(_("Wifi Password"))
        self.passwordEntry.connect("touch-event", self.give_name, self.passwordEntry    )


        eventBoxPsw = Gtk.EventBox()
        eventBoxPsw.connect("button-press-event", self.give_name, self.passwordEntry)
        eventBoxPsw.add(self.passwordEntry)


        content = Gtk.Label(name, name="info-dialog-content-label")
        content.set_line_wrap(True)
        content.set_justify(Gtk.Justification.CENTER)

        box = self.get_content_area()
        box.set_spacing(20)
        box.set_name("info-dialog-content-box")
        box.add(title)
        box.add(content)
        self.show_all()

    def give_name(self,a,b,entryName):

        # for child in self.this.scrolBox.get_children():
        #     self.this.scrolBox.remove(child)
        # self.this._screen.show_keyboard()
        # self.this.content.show_all()
        # box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # box.set_size_request(self.this._screen.gtk.content_width, self.this._screen.gtk.keyboard_height)


        # box.get_style_context().add_class("keyboard_box")
        # box.add(Keyboard(self.this._screen, self.remove_keyboard, entry=entryName))
        # self.this.scrolBox.pack_end(box, False, False, 0)
        # self.this.content.show_all()
        #subprocess.Popen("onboard")
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
