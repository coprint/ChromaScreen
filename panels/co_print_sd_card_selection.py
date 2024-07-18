import json
import logging
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ks_includes.screen_panel import ScreenPanel

# def create_panel(*args):
#     return CoPrintSdCardSelection(*args)


# class CoPrintSdCardSelection(ScreenPanel):

class Panel(ScreenPanel):     
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
       
        initHeader = InitHeader (self, _('Writing to SD Card'), _('Insert the SD Card of your printer into ChromaScreen to change the program of your 3D printer.'), "sdkart")

        self.image = self._gtk.Image("usbokey", self._gtk.content_width * .25 , self._gtk.content_height * .25)
       
        
        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.pack_start(self.continueButton, False, False, 0)

        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_chip_selection')
        self.backButton.set_always_show_image (True)       
        mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainBackButtonBox.pack_start(self.backButton, False, False, 0)
        #----------Skip-Button--------        
        skipIcon = self._gtk.Image("forward-arrow", 35, 35)
        skipLabel = Gtk.Label(_("Skip"), name="bottom-menu-label")            
        skipButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        skipButtonBox.set_halign(Gtk.Align.CENTER)
        skipButtonBox.set_valign(Gtk.Align.CENTER)
        skipButtonBox.pack_start(skipLabel, False, False, 0)
        skipButtonBox.pack_start(skipIcon, False, False, 0)
        self.skipButton = Gtk.Button(name ="back-button")
        self.skipButton.add(skipButtonBox)
        self.skipButton.connect("clicked", self.on_click_back_button, "co_print_home_screen")
        self.skipButton.set_always_show_image (True)       
        mainBackButtonBox.pack_end(self.skipButton, False, False, 0)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.pack_start(mainBackButtonBox, False, False, 0)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(self.image, True, True, 25)
        main.pack_end(buttonBox, True, False, 15)
        
        
       
      
        self.content.add(main)
        self._screen.base_panel.visible_menu(False)
       

   
      
    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate
    
    
    def on_click_continue_button(self, continueButton):
        # try:
        #     f = open(self._screen.path_config, encoding='utf-8')
       
        #     self.config_data = json.load(f)
        #     self.config_data[self._screen.selected_wizard_printer] = True
        #     json_object = json.dumps(self.config_data, indent=4)
 
          

        #     with open(self._screen.path_config, "w") as outfile:
        #         outfile.write(json_object)

        # except Exception as e:
        #     logging.exception(e) 
        self._screen.show_panel("co_print_printing_selection", "co_print_printing_selection", None, 2)
        
   
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)