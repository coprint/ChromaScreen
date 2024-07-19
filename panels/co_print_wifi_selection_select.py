import logging
import os
import subprocess


import gi
from ks_includes.widgets.infodialog import InfoDialog

from ks_includes.widgets.initheader import InitHeader
from ks_includes.widgets.keyboard import Keyboard
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintWifiSelectionSelect(*args)


# class CoPrintWifiSelectionSelect(ScreenPanel):
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

        initHeader = InitHeader (self, _('Connection Settings'),_('Connect the device by entering the information of the network you are using.'), "wifi")
        
        # ComboBox'a öğeler ekle
        
        self.selectedWifiImage = self._gtk.Image("sinyal", self._gtk.content_width * .05 , self._gtk.content_height * .05)
        self.selectedWifiName = Gtk.Label("",name ="wifi-labell")
        self.selectedWifiName.set_alignment(0,0.5)
        self.selectedWifiImage.set_alignment(1,0.5)

        self.entry = Gtk.Entry(name="device-name")
        self.entry.connect("activate", self.rename)
        self.entry.connect("touch-event", self.give_name)
        #self.entry.connect("focus-in-event", self._screen.show_keyboard)

        eventBox = Gtk.EventBox()
        eventBox.connect("button-press-event", self.give_name)
        eventBox.add(self.entry)


        self.selectedWifiBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0, name= 'wifi')
    
        self.selectedWifiBox.pack_start(self.selectedWifiName, True, True, 5)
        self.selectedWifiBox.pack_end(self.selectedWifiImage, True, True, 15)
        self.selectedWifiBox.pack_end(eventBox, True, True, 15)
        self.selectedWifiBox.set_size_request(150, 70)
        self.selectedWifiBox.set_margin_left(self._gtk.action_bar_width *2.6)
        self.selectedWifiBox.set_margin_right(self._gtk.action_bar_width*2.6)
        
        
        
       
        refreshButton = Gtk.Button(_('Back'),name ="flat-button-blue")
        refreshButton.connect("clicked", self.on_click_back_button)
       
       
        
        self.continueButton = Gtk.Button(_('Connect'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
    
        self.buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.buttonBox.set_halign(Gtk.Align.CENTER)
        self.buttonBox.pack_start(self.continueButton, False, False, 0)
        self.buttonBox.pack_start(refreshButton, False, False, 0)

        self.tempBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.tempBox.pack_start(self.buttonBox, False, False, 0)

        self.main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.main.pack_start(initHeader, False, False, 0)
        self.main.pack_end(self.tempBox, False, True, 10)
        self.main.pack_end(self.selectedWifiBox, False, True, 10)
       
        

        
        self.content.add(self.main)
       
    def initialize(self, items):
        self.selectedMenu = items
        self.selectedWifiName.set_label('')
    

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
            
        self.tempBox.pack_start(self.buttonBox, False, False, 0)
        self.content.show_all()

    def rename(self, widget):
        params = {"source": self.source, "dest": f"gcodes/{self.labels['new_name'].get_text()}"}
    def on_click_back_button(self, button):
        
        self._screen.show_panel("co_print_wifi_selection", "co_print_wifi_selection", None, 1, True)
    
    def execute_command_and_show_output(self):
        try:
            status = self.connect_to(self.selectedMenu, self.password)
            
            if status:
                self.close_dialog(self.waitDialog)
                self._screen.show_panel("co_print_wifi_selection_connect", "co_print_wifi_selection_connect", None, 1, False, items=self.selectedMenu, password=self.password)
            else:
                self.close_dialog(self.waitDialog)
                self.showMessageBox(_('Connection failed.'))
           
           
        except subprocess.CalledProcessError as e:
            self.showMessageBox(e.output.decode("utf-8"))
            
    def close_dialog(self, dialog):
        dialog.response(Gtk.ResponseType.CANCEL)
        dialog.destroy()  

    def showMessageBox(self, message):
        self.dialog = InfoDialog(self, message, True)
        self.dialog.get_style_context().add_class("alert-info-dialog")

        self.dialog.set_decorated(False)
        self.dialog.set_size_request(0, 0)
        timer_duration = 3000
        GLib.timeout_add(timer_duration, self.close_dialog, self.dialog)
        response = self.dialog.run()

    def on_click_continue_button(self, continueButton):
        
        self.password = self.entry.get_text()
        
        
        #self.execute_command_and_show_output()

        GLib.idle_add(self.execute_command_and_show_output)  
        self.waitDialog = InfoDialog(self, _("Please Wait"), True)
        self.waitDialog.get_style_context().add_class("alert-info-dialog")

        self.waitDialog.set_decorated(False)
        self.waitDialog.set_size_request(0, 0)
        response = self.waitDialog.run()


        


        
    
    def what_wifi(self):
        process = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)
        if process.returncode == 0:
            return process.stdout.decode('utf-8').strip()
        else:
            return ''

    def is_connected_to(self, ssid: str):
        return 'yes:'+ ssid in  self.what_wifi()

    def scan_wifi():
        process = subprocess.run(['nmcli', '-t', '-f', 'SSID,SECURITY,SIGNAL', 'dev', 'wifi'], stdout=subprocess.PIPE)
        if process.returncode == 0:
            return process.stdout.decode('utf-8').strip().split('\n')
        else:
            return []
            
    def is_wifi_available(self, ssid: str):
        return ssid in [x.split(':')[0] for x in self.scan_wifi()]

    def connect_to(self, ssid: str, password: str):
        
        subprocess.call(['nmcli', 'd', 'wifi', 'connect', ssid, 'password', password])
        return self.is_connected_to(ssid)

    def connect_to_saved(self, ssid: str):
        if not self.is_wifi_available(ssid):
            return False
        subprocess.call(['nmcli', 'c', 'up', ssid])
        return self.is_connected_to(ssid)
        

       
        
   
    
  