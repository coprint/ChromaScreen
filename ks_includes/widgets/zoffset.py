import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GdkPixbuf


class zOffset(Gtk.Box):
  

    def __init__(self, this):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.printer = this
        labelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        image = this._gtk.Image("zoffset", 35, 35)
        label = Gtk.Label(("Z Offset"), name="zoffset-label")
        labelBox.pack_start(image, True, False, 10)
        labelBox.pack_start(label, True, False, 0)
        labelBox.set_valign(Gtk.Align.CENTER)
        labelBox.set_halign(Gtk.Align.CENTER)
        
        
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.set_name("up-down-buttons-box")
        
        downIcon = this._gtk.Image("moveust", this._screen.width *.04, this._screen.width *.04)
        upIcon = this._gtk.Image("movealt", this._screen.width *.04, this._screen.width *.04)
        #downIcon = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size("styles/z-bolt/images/moveust.png", this._screen.width *.04, this._screen.width *.04))
        #upIcon = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size("styles/z-bolt/images/movealt.png", this._screen.width *.04, this._screen.width *.04))
        
        
        downButton = Gtk.Button(name ="up-down-buttons")
        downButton.set_image(downIcon)
        downButton.set_always_show_image(True)
        downButton.connect("clicked", self.on_button_clicked, 0.05)
        buttonBox.add(downButton)
        
        buttonBox.add(this._gtk.Image("zoffset", this._screen.width *.04, this._screen.width *.04))
        
        upButton = Gtk.Button(name ="up-down-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)
        upButton.connect("clicked", self.on_button_clicked, -0.05)
        buttonBox.add(upButton)
        
        self.entry = Gtk.Entry()
        self.entry.get_style_context().add_class("zoffset-entry")
        self.entry.set_text("0.0")
        # set_alignment ile input içindeki değer ortalanır
        self.entry.set_alignment(0.5)
        # set_width_chars(5) ile inputun genişliği 5 karakter genişliğinde ayarlandı
        self.entry.set_width_chars(8)
        self.entry.set_editable(False)
        self.entry.set_can_focus(False)
        
        inputBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        inputBox.add(buttonBox)
        inputBox.add(self.entry)
        
        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main.set_hexpand(True)
        main.set_valign(Gtk.Align.START)
        #main.set_size_request(this._screen.width *.5, -1)
        main.pack_start(labelBox, False, True, 0)
        main.pack_end(inputBox, False, True, 0)
        
       
        self.add(main)

    def on_button_clicked(self, widget, value):
            # Mevcut değeri alın
            #current_value = float(self.entry.get_text())
            current_value = float(self.printer._printer.data["gcode_move"]["homing_origin"][2])
            # Yeni değeri hesaplayın

            if(self.printer.OffsetConstant):
                if value >0:
                    new_value = current_value + self.printer.OffsetConstant 
                    increment = self.printer.OffsetConstant
                else:
                    new_value = current_value - self.printer.OffsetConstant 
                    increment = self.printer.OffsetConstant
            else:
                new_value = current_value + value
                increment = value
            direction = '-'
            if value > 0:
                 direction = '+'
                
            self.printer._screen._ws.klippy.gcode_script(f"SET_GCODE_OFFSET Z_ADJUST={direction}{abs(increment)} MOVE=1")
            
            
            # Yeni değeri entry'ye ayarlayın
            self.entry.set_text('{:.2f}'.format(new_value))
    def updateValue(self, value):
        current_value = value
        self.entry.set_text('{:.2f}'.format(current_value))

    