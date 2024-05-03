import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class Macros(Gtk.Box):
  

    def __init__(self, this, _macroName):
        super().__init__()
        
        macroBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        
       
            
        macroLabel = Gtk.Label(_macroName, name="wifi-name-label")
        macroLabel.set_justify(Gtk.Justification.LEFT)
        macroLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        macroLabelBox.pack_start(macroLabel, False, False, 0)
        
      
        macroButton = Gtk.Button(_("Execute"),name ="advanced-setting-button")
        macroButton.connect("clicked", this.run_gcode_macro, _macroName)
        
        
        macroBox.set_name("wifi-card-boxx")
        macroBox.pack_start(macroLabelBox, False, False, 0)
        macroBox.pack_end(macroButton, False, False, 0)
        macroBox.set_valign(Gtk.Align.CENTER)
        

        self.add(macroBox)

    