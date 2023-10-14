import logging
import os
import gi
from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.widgets.infodialog import InfoDialog
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class MainButton(Gtk.Box):
  

    def __init__(self,this, _image, _label, _style, _clickMenu, _imageDimension, _isOpenDialog):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.parent = this
        
        
        if _isOpenDialog:
            Button = this._gtk.Button(_image, _label, _style, _imageDimension)
            Button.connect("clicked", self.open_info_dialog)
            buttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            buttonBox.set_name("main-button-box")
            buttonBox.add(Button)
            self.add(buttonBox)
        else:
            Button = this._gtk.Button(_image, _label, _style, _imageDimension)
            Button.connect("clicked", self.on_click_menu_button, _clickMenu)
            buttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            buttonBox.set_name("main-button-box")
            buttonBox.add(Button)
            self.add(buttonBox)
        
        
        
    def on_click_menu_button(self, button, data):
     

        if(data == 'co_print_printing_screen' and self.parent._printer.state != 'printing'):
            data = 'co_print_printing_files_screen'
       
            
        self.parent._screen.show_panel(data, data, "Language", 1, False)

    def open_info_dialog(self, widget):
        self.dialog = InfoDialog(self.parent, ("Printer is returning to the starting position, please wait.."), False)
        self.dialog.get_style_context().add_class("alert-info-dialog")
        self.home()
        self.dialog.set_decorated(False)
        self.dialog.set_size_request(0, 0)
      
     

        response = self.dialog.run()
 
       
        
    def home(self):
        self.parent._screen._ws.klippy.gcode_script(KlippyGcodes.HOME, self.finished)
        
    def finished(self,asd,a,b):
        self.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.destroy()