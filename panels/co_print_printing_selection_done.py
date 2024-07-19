import json
import logging
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ks_includes.screen_panel import ScreenPanel

# def create_panel(*args):
#     return CoPrintPrintingSelectionDone(*args)


# class CoPrintPrintingSelectionDone(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
       
        initHeader = InitHeader (self, _('Setup Completed'), _("Setup for your 3D printer is complete. If you're not sure about the printer settings,you can exit without saving the settings using the Skip button"), "")

        self.image = self._gtk.Image("setupdone", self._gtk.content_width * .25 , self._gtk.content_height * .25)
       
        
        self.doneButton = Gtk.Button(_('Done'),name ="flat-button-blue")
        self.doneButton.connect("clicked", self.on_click_done_button)
        self.doneButton.set_hexpand(True)

        self.skipButton = Gtk.Button(_('Skip'),name ="flat-button-yellow-skip")
        self.skipButton.connect("clicked", self.on_click_skip_button)
        self.skipButton.set_hexpand(True)

        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        buttonBox.set_halign(Gtk.Align.CENTER)
        buttonBox.pack_start(self.doneButton, False, False, 0)
        buttonBox.pack_start(self.skipButton, False, False, 0)

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
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.pack_start(self.image, True, True, 25)
       
        main.pack_start(initHeader, False, False, 0)
       
        main.pack_end(buttonBox, False, False, 55)
        
        
       
      
        self.content.add(main)
        self._screen.base_panel.visible_menu(False)
       

   
      
    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate
    
    
    def on_click_done_button(self, continueButton):
        try:
            f = open(self._screen.path_config, encoding='utf-8')
       
            self.config_data = json.load(f)
            self.config_data[self._screen.selected_wizard_printer] = True
            json_object = json.dumps(self.config_data, indent=4)
 
          

            with open(self._screen.path_config, "w") as outfile:
                outfile.write(json_object)

        except Exception as e:
            logging.exception(e) 
        self._screen._ws.klippy.restart_firmware()
        self._screen.show_panel("co_print_home_screen", "co_print_home_screen", None, 2)
    
    def on_click_skip_button(self, continueButton):
        self._screen._ws.klippy.restart_firmware()
        self._screen.show_panel("co_print_home_screen", "co_print_home_screen", None, 2)
        
   
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)