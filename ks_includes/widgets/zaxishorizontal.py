import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GdkPixbuf


class zAxisHorizontal(Gtk.Box):
  

    def __init__(self, this, _zoffsetIconVisibility):
        super().__init__()
    
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.set_name("z-axis-horizontal-button-box")
        self.printer = this
        upIcon = this._gtk.Image("moveust", this._screen.width *.045, this._screen.width *.045)
        downIcon = this._gtk.Image("movealt", this._screen.width *.045, this._screen.width *.045)
        
        upButton = Gtk.Button(name ="up-down-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)

       
        upButton.connect("clicked", self.on_button_clicked, -0.05, '+')
        buttonBox.add(upButton)
    
        if _zoffsetIconVisibility:
            zOffsetImage = this._gtk.Image("zoffset", this._screen.width *.05, this._screen.width *.05)
            zOffsetImage_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            zOffsetImage_box.set_halign(Gtk.Align.CENTER)
            zOffsetImage_box.add(zOffsetImage)
           
            buttonBox.add(zOffsetImage_box)
        
        downButton = Gtk.Button(name ="up-down-buttons")
        downButton.set_image(downIcon)
        downButton.set_always_show_image(True)
        downButton.connect("clicked", self.on_button_clicked, 0.05, '-')
        buttonBox.add(downButton)
        

        
        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main.set_valign(Gtk.Align.CENTER)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(buttonBox, False, False, 10)
        
       
        self.add(main)

    def on_button_clicked(self, widget, value, direction):
            # Mevcut değeri alın
            #current_value = float(self.entry.get_text())
            current_value = float(self.printer._printer.data["gcode_move"]["homing_origin"][2])
            # Yeni değeri hesaplayın
            if hasattr(self.printer, "distance"):
                 value = self.printer.distance
            if hasattr(self.printer, "OffsetConstant"):
                value = self.printer.OffsetConstant
            
            new_value = current_value + value    
            self.printer._screen._ws.klippy.gcode_script(f"SET_GCODE_OFFSET Z_ADJUST={direction}{abs(value)} MOVE=1")
            
            
            # if hasattr(self.printer, "zoffset"):
            #     self.printer.zoffset.set_label('{:.3f}'.format(new_value))
    def updateValue(self, value):
        current_value = value
        self.entry.set_text('{:.2f}'.format(current_value))

    