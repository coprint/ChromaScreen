import crypt
import json
import logging
import os
from signal import SIGTERM
import subprocess


import gi

from ks_includes.widgets.initheader import InitHeader
from ks_includes.widgets.keyboard import Keyboard
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintProductNaming(*args)


# class CoPrintProductNaming(ScreenPanel):
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

       
        
        initHeader = InitHeader (self, _('Rename Your Device'),_('Please specify a custom name for your device.'), "naming")

        self.deviceImage = self._gtk.Image("device", self._gtk.content_width * .4 , self._gtk.content_height * .4)
       
        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        self.buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.buttonBox.pack_start(self.continueButton, False, False, 0)
   
        
        self.entry = Gtk.Entry(name="device-name")
        self.entry.connect("activate", self.rename)
        self.entry.connect("focus-in-event", self.give_name)
        self.entry.set_width_chars(5)
        self.entry.set_placeholder_text(("Device Name"))
        self.entry.set_margin_left(self._gtk.action_bar_width *3)
        self.entry.set_margin_right(self._gtk.action_bar_width *3)

        eventBox = Gtk.EventBox()
        eventBox.connect("button-press-event", self.give_name)
        eventBox.add(self.entry)
        
        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_region_selection')
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
        
        self.tempBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.tempBox.pack_start(self.deviceImage, False, False, 0)
        self.tempBox.pack_start(self.buttonBox, False, False, 0)

        self.main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main.pack_start(mainBackButtonBox, False, False, 0)
        self.main.pack_start(initHeader, False, False, 0)
        self.main.pack_start(eventBox, False, False, 5)
        self.main.pack_start(self.tempBox, False, False, 0)
   

        self.content.add(self.main)
    


    def give_name(self,a,b):
       
        for child in self.tempBox.get_children():
            self.tempBox.remove(child) 
        self._screen.show_keyboard()
        self.content.show_all()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_size_request(self._screen.gtk.content_width, self._screen.gtk.keyboard_height)

       
        box.get_style_context().add_class("keyboard_box")
        box.add(Keyboard(self._screen, self.remove_keyboard, entry=self.entry))
        self.tempBox.pack_end(box, False, False, 0)
        self.content.show_all()

    def remove_keyboard(self, widget=None, event=None):
        for child in self.tempBox.get_children():
            self.tempBox.remove(child) 
        self.tempBox.pack_start(self.deviceImage, False, False, 0)
        self.tempBox.pack_start(self.buttonBox, False, False, 0)
        self.content.show_all()


    def rename(self, widget):
        params = {"source": self.source, "dest": f"gcodes/{self.labels['new_name'].get_text()}"}
       

    def on_click_continue_button(self, continueButton):

        logging.debug(f"Device Name: " + self.entry.get_text())

       
        
        try:
            f = open(self._screen.path_config, encoding='utf-8')
       
            self.config_data = json.load(f)
            self.config_data['InitConfigDone'] = True
            json_object = json.dumps(self.config_data, indent=4)
 
          
            with open(self._screen.path_config, "w") as outfile:
                outfile.write(json_object)

        except Exception as e:
            logging.exception(e) 

        self._screen.show_panel("co_print_wifi_selection", "co_print_wifi_selection", None, 1,False)
        
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)
