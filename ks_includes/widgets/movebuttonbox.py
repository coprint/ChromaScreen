import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GdkPixbuf


class MoveButtonBox(Gtk.Box):
  

    def __init__(self, _label, _btn1, _btn2, _btn3, _btn4, _buttonStyle, this):
        super().__init__()
        
        
        self.printer = this

        
        labelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        labelBox.set_valign(Gtk.Align.CENTER)
        labelBox.set_name("move-label-box")
        
        label = Gtk.Label(_label, name="move-label")
        label.set_max_width_chars(1)
        label.set_line_wrap(True)
        label.set_justify(Gtk.Justification.CENTER)
        labelBox.pack_start(label, True, False, 0)
        self.printer.distance = _btn2
        self.prev_distance = _btn2
        
        self.buttons = {f"{_btn1}": Gtk.Button(_btn1, name =_buttonStyle),
                        f"{_btn2}": Gtk.Button(_btn2, name =_buttonStyle),
                        f"{_btn3}": Gtk.Button(_btn3, name =_buttonStyle),
                        f"{_btn4}": Gtk.Button(_btn4, name =_buttonStyle)
        }
   
        self.buttons[f"{_btn1}"].connect("clicked", self.change_distance, _btn1)
        self.buttons[f"{_btn2}"].connect("clicked", self.change_distance, _btn2)
        self.buttons[f"{_btn3}"].connect("clicked", self.change_distance, _btn3)
        self.buttons[f"{_btn4}"].connect("clicked", self.change_distance, _btn4)
        self.buttons[f"{_btn2}"].get_style_context().add_class("move-button-active")
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(labelBox, True, False, 0)
        main.pack_start(self.buttons[f"{_btn1}"], True, False, 0)
        main.pack_start(self.buttons[f"{_btn2}"], True, False, 0)
        main.pack_start(self.buttons[f"{_btn3}"], True, False, 0)
        main.pack_start(self.buttons[f"{_btn4}"], True, False, 0)
        
        
       
        self.add(main)

    def change_distance(self, widget, distance):
        logging.info(f"### Distance {distance}")
        self.buttons[f"{self.prev_distance}"].get_style_context().remove_class("move-button-active")
        self.buttons[f"{distance}"].get_style_context().add_class("move-button-active")
        self.prev_distance = distance
        if(self.printer.distance):
            self.printer.distance = distance
        if(self.printer.distanceLabel):
            self.printer.distanceLabel.set_label(str(distance))
            

    