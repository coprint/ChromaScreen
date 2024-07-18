import logging
import os

import gi
from ks_includes.widgets.keypad_new import KeyPadNew
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GdkPixbuf


class ProgressBar(Gtk.Box):
  

    def __init__(self, this, _temperature, _image, _fraction, _style, numpad_method):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.numpad_method = numpad_method
        self.progress = this
        self.label = Gtk.Label(_temperature,name ="progress-label")
        self.scale_progress = Gtk.ProgressBar(name =_style)
        self.scale_progress.set_fraction(_fraction)
        self.scale_progress.set_show_text(False)
        self.scale_progress.set_hexpand(True)
        
        numPadIcon = this._gtk.Image("calculator", this._screen.width *.03, this._screen.width *.03)
        # numPadButton = Gtk.Button(name ="progress-numpad")
        # numPadButton.connect("clicked", self.open_numpad)
        # numPadButton.set_image(numPadIcon)
        # numPadButton.set_always_show_image(True)
        
        extruder_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        extruder_box.set_hexpand(True)
        extruder_box.set_valign(Gtk.Align.CENTER)
        extruder_box.add(this._gtk.Image(_image, 30, 30))
        extruder_box.add(self.label)
        extruder_box.add(self.scale_progress)
        extruder_box.add(numPadIcon)
        extruder_event_box = Gtk.EventBox()
        extruder_event_box.connect("button-press-event", self.open_numpad)
        extruder_event_box.add(extruder_box)
        # printerConnectionEventBox = Gtk.EventBox()
        # printerConnectionEventBox.connect("button-press-event", self.change_page)
        # printerConnectionEventBox.add(printerConnectionBox)
        self.add(extruder_event_box)
        
       
        # self.add(extruder_box)

    
    def updateValue(self, value, label):
        self.scale_progress.set_fraction(value)
        self.label.set_text(label)

    def open_numpad(self, widget, event):
        
        dialog = KeyPadNew(self.progress)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            self.numpad_method(int(dialog.resp))
            
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
       
        dialog.destroy()   
    