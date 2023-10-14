import logging
import os
from ks_includes.widgets.keypad_new import KeyPadNew
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class CounterInput(Gtk.Box):
  

    def __init__(self, this, _unit, _title, _input, script, multiplier):
        super().__init__()
        self.printing = this
        self.script = script
        self.unit = Gtk.Label(_unit, name="counter-input-label")
        self.label = Gtk.Label(_input, name="counter-input-label")
        
        
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        buttonBox.set_spacing(-13)
        buttonBox.set_name("counter-input-buttons-box")
        
        downIcon = this._gtk.Image("moveust", this._screen.width *.03, this._screen.width *.03)
        upIcon = this._gtk.Image("movealt", this._screen.width *.03, this._screen.width *.03)
        
        downButton = Gtk.Button(name ="counter-up-down-buttons")
        downButton.set_image(downIcon)
        downButton.set_always_show_image(True)
        downButton.connect("clicked", self.on_button_clicked, multiplier)
        buttonBox.add(downButton)
        
        upButton = Gtk.Button(name ="counter-up-down-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)
        upButton.connect("clicked", self.on_button_clicked, -1* multiplier)
        buttonBox.add(upButton)
        
        numPadIcon = this._gtk.Image("calculator", this._screen.width *.03, this._screen.width *.03)
        numPadButton = Gtk.Button(name ="speed-factor-button")
        numPadButton.connect("clicked", self.open_numpad)
        numPadButton.set_image(numPadIcon)
        numPadButton.set_always_show_image(True)
     
        frame = Gtk.Frame(name="counter-frame")
        frame.set_label(_title)
        frame.set_label_align(0.1, 0.5)

        
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        vbox.pack_start(self.label, False, False, 0)
        vbox.pack_end(numPadButton, False, False, 0)
        vbox.pack_end(self.unit, False, False, 0)
        vbox.set_name("counter-input-box")
        frame.add(vbox)
                

        selectBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        selectBox.pack_start(frame, True, False, 0)
        selectBox.pack_start(buttonBox, False, False, 0)
       
        

        self.add(selectBox)

    def on_button_clicked(self, widget, value):
            # Mevcut değeri alın
            #current_value = float(self.entry.get_text())
            current_value = int(self.label.get_label())
            # Yeni değeri hesaplayın
            new_value = current_value + value
            direction = '-'
            if value > 0:
                 direction = '+'
            self.printing._screen._ws.klippy.gcode_script(f"{self.script}{new_value}")
            
            
            # Yeni değeri entry'ye ayarlayın
            self.label.set_label(str(new_value))
    def updateValue(self, value):
        
        
        self.label.set_label(str(value))

    def getValue(self):
        
        
        return int(self.label.get_label())

    def open_numpad(self, widget):
        
        dialog = KeyPadNew(self.printing)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            resp = dialog.resp
            self.label.set_label(resp)
            self.printing._screen._ws.klippy.gcode_script(f"{self.script}{int(resp)}")
            
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
       
        dialog.destroy()