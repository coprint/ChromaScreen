import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class InitHeader(Gtk.Box):
  

    def __init__(self, this, _subTitle, _subText, _imageName=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        
        subTitle = Gtk.Label(_subTitle, name="init-header-subtitle-label")
        subText = Gtk.Label(_subText,name ="init-header-subtext-label")
        subText.set_justify(Gtk.Justification.CENTER)
        subText.set_line_wrap(True)
        subText.set_max_width_chars(60)
     

        selectBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
       
        if _imageName is not None:
            image = this._gtk.Image(_imageName, this._gtk.content_width * .15 , this._gtk.content_height * .15)
            selectBox.pack_start(image, False, True, 2)

        selectBox.pack_end(subText, False, True, 2)
        selectBox.pack_end(subTitle, False, True, 2)
        selectBox.set_halign(Gtk.Align.CENTER)
        

        self.add(selectBox)

    