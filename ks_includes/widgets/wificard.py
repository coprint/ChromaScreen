import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class WifiCard(Gtk.Box):
  

    def __init__(self, this, _image, _wifiName, _connectStatus):
        super().__init__()

        image = this._gtk.Image(_image, this._gtk.content_width * .08 , this._gtk.content_height * .08)
        
        wifiNameLabel = Gtk.Label(_wifiName, name="wifi-name-label")
        wifiNameLabel.set_justify(Gtk.Justification.LEFT)
        wifiNameLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        wifiNameLabelBox.pack_start(wifiNameLabel, False, False, 0)
        
        connectStatusLabel = Gtk.Label(_connectStatus, name ="wifi-status-label")
        connectStatusLabel.set_justify(Gtk.Justification.LEFT)
        connectStatusLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        connectStatusLabelBox.pack_start(connectStatusLabel, False, False, 0)
        
        wifiLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        wifiLabelBox.pack_start(wifiNameLabelBox, False, False, 0)
        wifiLabelBox.pack_start(connectStatusLabelBox, False, False, 0)

        wifiCardBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
      
        wifiCardBox.set_name("wifi-card-box")
        wifiCardBox.pack_start(wifiLabelBox, False, False, 0)
        wifiCardBox.pack_end(image, False, False, 0)
    
        
        cartesianTypeEventBox = Gtk.EventBox()
        cartesianTypeEventBox.connect("button-press-event", this.wifiChanged, _wifiName)
        cartesianTypeEventBox.add(wifiCardBox)


        self.add(cartesianTypeEventBox)

    