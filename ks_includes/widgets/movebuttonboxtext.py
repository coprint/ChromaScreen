import logging
from ks_includes.widgets.keypad_new import KeyPadNew
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
class MoveButtonBoxText(Gtk.Box):
    def __init__(self, _label, _btn1, _btn2, _btn3, _btn4, _buttonStyle, this):
        super().__init__()
        self.printer = this
        numPadIcon = this._gtk.Image("calculator", this._screen.width *.03, this._screen.width *.03)
        numPadButton = Gtk.Button(name ="speed-factor-button")
        numPadButton.connect("clicked", self.open_numpad)
        numPadButton.set_image(numPadIcon)
        numPadButton.set_always_show_image(True)
        labelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        labelBox.set_valign(Gtk.Align.CENTER)
        labelBox.set_name("move-label-box")
        label = Gtk.Label(_label, name="move-label")
        label.set_max_width_chars(1)
        label.set_line_wrap(True)
        label.set_justify(Gtk.Justification.CENTER)
        labelBox.pack_start(label, True, False, 0)
        self.printer.speed = _btn2
        self.printer.name = _btn2
        self.btn4 = _btn4
        self.buttons = {f"{_btn1}": Gtk.Button(_btn1, name =_buttonStyle),
                        f"{_btn2}": Gtk.Button(_btn2, name =_buttonStyle),
                        f"{_btn3}": Gtk.Button(_btn3, name =_buttonStyle),
                        f"custom": Gtk.Button(self.btn4, name =_buttonStyle)
        }
        btn4Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        btn4Box.pack_start(self.buttons[f"custom"], False, False, 0)
        btn4Box.pack_start(numPadButton, False, False, 0)
        self.buttons[f"{_btn1}"].connect("clicked", self.change_distance, _btn1)
        self.buttons[f"{_btn2}"].connect("clicked", self.change_distance, _btn2)
        self.buttons[f"{_btn3}"].connect("clicked", self.change_distance, _btn3)
        self.buttons[f"custom"].connect("clicked", self.change_distance, 'custom')
        self.buttons[f"{_btn2}"].get_style_context().add_class("move-button-active")
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(labelBox, True, False, 0)
        main.pack_start(self.buttons[f"{_btn1}"], True, False, 0)
        main.pack_start(self.buttons[f"{_btn2}"], True, False, 0)
        main.pack_start(self.buttons[f"{_btn3}"], True, False, 0)
        main.pack_start(btn4Box, True, False, 0)
        self.add(main)

    def open_numpad(self, widget):
        dialog = KeyPadNew(self.printer)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            resp = dialog.resp
            self.btn4 = resp
            self.buttons[f"{self.printer.name}"].get_style_context().remove_class("move-button-active")
            self.buttons[f"custom"].get_style_context().add_class("move-button-active")
            self.printer.speed = int(resp)
            self.buttons[f"custom"].set_label(resp)
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        dialog.destroy()

    def change_distance(self, widget, distance):
        self.buttons[f"{self.printer.name}"].get_style_context().remove_class("move-button-active")
        self.buttons[f"{distance}"].get_style_context().add_class("move-button-active")
        self.printer.name = distance
        logging.info(f"### Distance {distance}")
        if(distance == 'custom'):
            distance = self.btn4
        self.printer.speed = distance