import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Pango


class CheckButtonBox(Gtk.Box):
  

    def __init__(self, this, _content, onCheck=None):
        super().__init__()
        self.onCheck = onCheck
        self.button1 = Gtk.CheckButton(label=_content)
      
        
        self.button1.connect("toggled", self.on_button_toggled)
        
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        info.set_halign(Gtk.Align.START)
        
        info.pack_start(self.button1, False, False, 0)

        self.add(info)

    def on_button_toggled(self, button):
        if(self.onCheck is not None):
            self.onCheck(button.get_active())

        if button.get_active():
            print("Radio butonu seçildi:", button.get_label())
            

    