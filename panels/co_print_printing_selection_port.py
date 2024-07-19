import logging
import os
import subprocess
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintPrintingSelectionPort(*args)


# class CoPrintPrintingSelectionPort(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
       
        initHeader = InitHeader (self, _('Connect Your 3D Printer'), _('Connect your 3D printer to Co Print Smart using a USB cable.'), "yazicibaglama")

         
        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        self.refreshButton = Gtk.Button(_('Refresh'),name ="flat-button-blue")
        self.refreshButton.connect("clicked", self.control_usb)
        self.refreshButton.set_hexpand(True)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.pack_start(self.continueButton, False, False, 0)
        buttonBox.pack_end(self.refreshButton, False, False, 0)

       

        self.portOne = Gtk.Button("---",name ="flat-button-black")
       
        self.portOne.set_hexpand(True)
        portOneBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        portOneBox.pack_start(self.portOne, False, False, 0)


        self.portTwo = Gtk.Button("---",name ="flat-button-black")
        
        self.portTwo.set_hexpand(True)
        portTwoBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        portTwoBox.pack_start(self.portTwo, False, False, 0)

        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_printing_selection')
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

        self.portBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.portBox.pack_start(portOneBox, False, False, 0)
        # self.portBox.pack_start(portTwoBox, False, False, 5)


        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
       
       
       
        main.pack_start(mainBackButtonBox, False, False, 0)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(self.portBox, False, False, 0)
        main.pack_end(buttonBox, False, True, 30)
       
        GLib.timeout_add_seconds(1, self.control_usb, None)
        self.content.add(main)
        self._screen.base_panel.visible_menu(False)
    def control_usb(self, args):
        command = 'ls /dev/serial/by-path/*'
       
        string = os.popen(command).read()
        print(string)
        array = string.split('\n')

        usb_parts = []
        for child in self.portBox.get_children():
            self.portBox.remove(child)
        grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=0,
                         row_spacing=0)
        if string != '':
            row = 0
            count = 0
            for part in array:
                parts = part.split('usb-')
                if len(parts) > 1:
                    desired_part = parts[1]
                    usb_parts.append('usb-' + desired_part)
                    self.portTwo = Gtk.Button('usb-' + desired_part,name ="flat-button-black")
                    self.portTwo.set_hexpand(True)
                    self.portTwo.connect("clicked", self.on_click_select_path, part)
                    portTwoBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
                    portTwoBox.pack_start(self.portTwo, False, False, 0)
                    #self.portBox.add(portTwoBox)
                    grid.attach(portTwoBox,count,row,1,1)
                    count += 1
                    if count % 1 == 0:
                        count = 0
                        row += 1
            gridBox = Gtk.Box()
            gridBox.set_halign(Gtk.Align.CENTER)
            gridBox.add(grid)
            
            self.scroll = self._gtk.ScrolledWindow()
            self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            self.scroll.set_min_content_height(self._screen.height * .3)
            self.scroll.set_max_content_height(self._screen.height * .4)
            self.scroll.set_kinetic_scrolling(True)
            self.scroll.get_overlay_scrolling()
        
        
            self.scroll.add(gridBox)
            self.portBox.pack_start(self.scroll,False,False,0)
        else:
            self.portTwo = Gtk.Button('---',name ="flat-button-black")
            self.portTwo.set_hexpand(True)
            self.portTwo.connect("clicked", self.on_click_select_path, 'usb-1:0:1')
            portTwoBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            portTwoBox.pack_start(self.portTwo, False, False, 0)
            self.portBox.add(portTwoBox)
        

   
        
        
        
        self.content.show_all()
       

    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate
    
    
    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_printing_selection_done", "co_print_printing_selection_done", None, 1, True)
        
   
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)
    
    def update_mcu_serial(self, new_serial):
        # Dosyayı oku ve satırları bir liste olarak al
        file_path = os.path.join(os.path.expanduser("~/"), "printer_"+str(self._screen.selected_printer_index)+"_data", "config")
        with open(file_path+ "/printer.cfg", 'r') as file:
            lines = file.readlines()

        # Dosyanın içinde dolaşarak MCU serisi olan satırı bul
        for i, line in enumerate(lines):
            if line.strip().startswith("[mcu]"):
                # MCU serisini güncelle
                lines[i+1] = f"serial: {new_serial}\n"
                break

        # Dosyayı güncelle
        with open(file_path+ "/printer.cfg", 'w') as file:
            file.writelines(lines)
        self.on_click_continue_button(None)

    def on_click_select_path(self, button, data):
        
        self.update_mcu_serial(data)
        print(data)