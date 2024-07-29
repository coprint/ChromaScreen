import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class SystemSetting(Gtk.Box):
  

    def __init__(self, this, _macroName, _buttonName, _refreshButtonVisibility, name):
        super().__init__()
        
        macroBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        
        
        refreshIcon = this._gtk.Image("update", this._screen.width *.028, this._screen.width *.028)
        refreshButton = Gtk.Button(name ="setting-button")
        refreshButton.set_image(refreshIcon)
        refreshButton.set_always_show_image(True)
        refreshButton.connect("clicked", this.refresh_updates)
            
        macroLabel = Gtk.Label(_macroName, name="wifi-name-label")
        macroLabel.set_justify(Gtk.Justification.LEFT)
        macroLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        macroLabelBox.pack_start(macroLabel, False, False, 0)
        
        macroButton = Gtk.Button(_buttonName,name ="advanced-setting-button")
        macroButton.connect("clicked", this.VersionControl, name)
        
        macroButton.set_sensitive(_refreshButtonVisibility)
        
        
        macroBox.set_name("system-setting-card-box")
        macroBox.pack_start(macroLabelBox, False, False, 0)
        macroBox.pack_end(macroButton, False, False, 0)
        macroBox.pack_end(refreshButton, False, False, 10)
        macroBox.set_valign(Gtk.Align.CENTER)
        

        self.add(macroBox)

    