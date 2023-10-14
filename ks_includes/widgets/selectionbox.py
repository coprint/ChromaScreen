import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class SelectionBox(Gtk.Box):
  

    def __init__(self, this, _content, _imageName):
        super().__init__()

        image = this._gtk.Image(_imageName, this._gtk.content_width * .05, this._gtk.content_height * .05)
        content = Gtk.Label(_content,name ="selection-box-label")
        selectionBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        
        selectionBox.set_name("selection-box")
        selectionBox.pack_start(content, False, True, 10)
        selectionBox.pack_end(image, False, False, 10)

        self.add(selectionBox)
         

    