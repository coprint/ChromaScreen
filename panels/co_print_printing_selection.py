import logging
import os
import subprocess
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf
import pyudev
from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintPrintingSelection(*args)


# class CoPrintPrintingSelection(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
       
        initHeader = InitHeader (self, _('Connect Your 3D Printer'), _('Connect your 3D printer to Co Print Smart using a USB cable.'), "yazicibaglama")

        self.image = self._gtk.Image("printer-connect", self._gtk.content_width * .3 , self._gtk.content_height * .3)
       
        
        self.continueButton = Gtk.Button(_('Searching for Printer..'),name ="flat-button-yellow")
        #self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.pack_start(self.continueButton, False, False, 0)

        spinner = Gtk.Spinner()
        spinner.props.width_request = 50  
        spinner.props.height_request = 50
        spinner.start()

        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_printing_brand_selection_new')
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
        main.pack_start(self.image, False, False, 20)
        main.pack_end(buttonBox, True, False, 10)
        main.pack_end(spinner, False, False, 0)
        
        self.content.add(main)
        self._screen.base_panel.visible_menu(False)
        GLib.timeout_add_seconds(3, self.control_usb,None)
        #GLib.idle_add(self.control_usb, None)

   
    def control_usb(self, args):
        self.isSuccess= False
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb')
        device = monitor.poll(timeout=30)
        if device != None:
            
            if device.action == 'add':
               self.on_click_continue_button()
               self.isSuccess= True
               
                    
            if device.action == 'unbind':
                print('{} unbind'.format(device))
        if self.isSuccess  == False:
            GLib.timeout_add_seconds(1, self.control_usb, None)
        return False
    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate
    
    
    def on_click_continue_button(self):
        self._screen.show_panel("co_print_printing_selection_port", "co_print_printing_selection_port", None, 1, True)
        
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)
