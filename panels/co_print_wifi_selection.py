import logging
import os
import gi
import subprocess
from ks_includes.widgets.wificard import WifiCard
from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
import netifaces
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel

# def create_panel(*args):
#     return CoPrintWifiSelection(*args)


# class CoPrintWifiSelection(ScreenPanel):
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

      
        self.selectedWifiIndex = None
        self.wifies = []
        #wifi_list = subprocess.check_output(['nmcli', '-f', 'SSID', 'dev', 'wifi']).decode('utf-8')
        initHeader = InitHeader (self, _('Connection Settings'),_('Connect the device by entering the information of the network you are using.'), "wifi")
       

        wifi_flowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        wifi_flowbox.set_halign(Gtk.Align.CENTER)
        wifi_flowbox.set_hexpand(True)

        #wifi_list = wifi_list.split("\n")
        #wifi_list = list(filter(None, wifi_list))
        # for wifi in wifi_list:
        #     if(wifi != "SSID" or wifi != "--"):
        #         self.wifies.append({'Name': wifi, 'Icon': 'sinyal'})
                
        # for wifi in self.wifies:
        #     wifione = WifiCard(self, "signal-high", wifi['Name'], "Connected")
        #     wifi_flowbox.pack_start(wifione, True, True, 0)
        
        spinner = Gtk.Spinner()
        spinner.props.width_request = 100  
        spinner.props.height_request = 100
        spinner.start()

        GLib.idle_add(self.refresh, None)

        # wifione = WifiCard(self, "signal-high", "Co Print 5G", "Connected")
        # wifitwo = WifiCard(self, "signal-high", "TurkTelekom Wifi", "Click to connect.")
        # wifithree = WifiCard(self, "signal-medium", "Superonline Wifi", "Click to connect.")
        # wififour = WifiCard(self, "signal-medium", "Superonline Wifi", "Click to connect.")
        # wififive = WifiCard(self, "signal-medium", "Superonline Wifi", "Click to connect.")
        # wifisix = WifiCard(self, "signal-low", "Superonline Wifi2", "Click to connect.")
        # wifiseven = WifiCard(self, "signal-low", "Superonline Wifi2", "Click to connect.")


        # wifi_flowbox.pack_start(wifione, True, True, 0)
        # wifi_flowbox.pack_start(wifitwo, True, True, 0)
        # wifi_flowbox.pack_start(wifithree, True, True, 0)
        # wifi_flowbox.pack_start(wififour, True, True, 0)
        # wifi_flowbox.pack_start(wififive, True, True, 0)
        # wifi_flowbox.pack_start(wifisix, True, True, 0)
        # wifi_flowbox.pack_start(wifiseven, True, True, 0)
        
     
        self.scroll = self._gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_kinetic_scrolling(True)
        self.scroll.get_overlay_scrolling()
        #self.scroll.set_halign(Gtk.Align.CENTER)
        #self.scroll.set_min_content_width(self._screen.height * .3)
        self.scroll.add(spinner)
        
        refreshIcon = self._gtk.Image("update", self._screen.width *.028, self._screen.width *.028)
        refreshButton = Gtk.Button(name ="setting-button")
        refreshButton.connect("clicked", self.refresh)
        refreshButton.set_image(refreshIcon)
        refreshButton.set_always_show_image(True)
        refreshButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        refreshButtonBox.set_valign(Gtk.Align.CENTER)
        refreshButtonBox.add(refreshButton)
        
        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        buttonBox.set_halign(Gtk.Align.CENTER)
        buttonBox.pack_start(self.continueButton, False, False, 0)
        buttonBox.pack_start(refreshButtonBox, False, False, 0)

        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_product_naming')
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
                
        self.main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main.set_halign(Gtk.Align.CENTER)
        self.main.pack_start(initHeader, False, False, 0)
        self.main.pack_start(self.scroll, False, True, 10)
        self.main.pack_end(buttonBox, False, False, 10)
       

        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(mainBackButtonBox, False, False, 0)
        page.pack_start(self.main, False, True, 0)
        
        self.content.add(page)
       


    
    

    def wifiChanged(self,widget , event, name):
      
       self.selectedWifiIndex = name
       self._screen.show_panel("co_print_wifi_selection_select", "co_print_wifi_selection_select", None, 1, False, items=self.selectedWifiIndex)

    def on_click_continue_button(self, continueButton):
        # if self.selectedWifiIndex is not None:
        #     self._screen.show_panel("co_print_wifi_selection_select", "co_print_wifi_selection_select", None, 1, True, items=self.selectedWifiIndex)
        # else:
        #     #self._screen.show_panel("co_print_home_screen", "co_print_home_screen", None, 2)
        self._screen.show_panel("co_print_printing_brand_selection_new", "co_print_printing_brand_selection_new", None, 1,False)
       

    #asıl kullanılan metod bu diğer metodu sayfayı görüntülemek için yazdım
    def refresh(self, widget):

        spinner = Gtk.Spinner()
        spinner.props.width_request = 100  
        spinner.props.height_request = 100
        spinner.start()
        for child in self.scroll.get_children():
                self.scroll.remove(child)
        self.scroll.add(spinner)
        self.content.show_all()   

        GLib.idle_add(self.wifi_process)  
    
    def wifi_process(self):
        wifi_flowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        wifi_flowbox.set_halign(Gtk.Align.CENTER)
        wifi_flowbox.set_hexpand(True)
    
        self.wifies = []
        wifiNames = []
        wifi_list = subprocess.check_output(['nmcli', '-f', 'SSID,BARS', 'dev', 'wifi']).decode()
       
        
        if wifi_list != '':
            wifi_list = wifi_list.split("\n")
            connected_wifi_list = self.what_wifi()
            for wifi in wifi_list[1:]:
                wifiarray = wifi.split()
                if (len(wifiarray) > 0):
                    bar = wifiarray.pop()
                    name = ' '.join(wifiarray)
                    if (str(name) != "SSID" and str(name) != "--"):
                        icon = 'signal-low'
                        if (len(bar) == 4):
                            icon = 'signal-high'
                        if (len(bar) == 3):
                            icon = 'signal-medium'
                        if str(name) not in wifiNames:
                            wifiNames.append(str(name))
                            connectionStatus = self.is_connected_to(str(name), connected_wifi_list)
                            if connectionStatus:
                                self.wifies.insert(0, {'Name': str(name), 'Icon': icon,
                                                       'ConnectionStatus': connectionStatus})
                            else:
                                self.wifies.append(
                                    {'Name': str(name), 'Icon': icon, 'ConnectionStatus': connectionStatus})
                    
            for wifi in self.wifies:
                connection_button_visible = False
                connection_status = _('Not Connected')
                if wifi['ConnectionStatus']:
                    connection_status = _('Connected')
                    connection_button_visible = True

                wifione = WifiCard(self, wifi['Icon'], wifi['Name'], connection_status, connection_button_visible)

                wifi_flowbox.pack_start(wifione, False, False, 0)

           


        else:

            wifione = WifiCard(self, "signal-high", "Co Print 5G", "Connected")
            wifitwo = WifiCard(self, "signal-high", "TurkTelekom Wifi", "Click to connect.")
            wifithree = WifiCard(self, "signal-medium", "Superonline Wifi", "Click to connect.")
            wififour = WifiCard(self, "signal-medium", "Superonline Wifi", "Click to connect.")
            wififive = WifiCard(self, "signal-medium", "Superonline Wifi", "Click to connect.")
            wifisix = WifiCard(self, "signal-low", "Superonline Wifi2", "Click to connect.")
            wifiseven = WifiCard(self, "signal-low", "Superonline Wifi2", "Click to connect.")
            wifi_flowbox.pack_start(wifione, True, True, 0)
            wifi_flowbox.pack_start(wifitwo, True, True, 0)
            wifi_flowbox.pack_start(wifithree, True, True, 0)
            wifi_flowbox.pack_start(wififour, True, True, 0)
            wifi_flowbox.pack_start(wififive, True, True, 0)
            wifi_flowbox.pack_start(wifisix, True, True, 0)
            wifi_flowbox.pack_start(wifiseven, True, True, 0)
            for child in self.scroll.get_children():
                self.scroll.remove(child) 
        
        for child in self.scroll.get_children():
            self.scroll.remove(child)
        

    

        self.scroll.add(wifi_flowbox)
        self.content.show_all()  

    def what_wifi(self):
        process = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)
        if process.returncode == 0:
            return process.stdout.decode('utf-8').strip()
        else:
            return ''   
        
    def is_connected_to(self, ssid: str, wifi_list):
        return ('yes:' + ssid + "\n" in wifi_list) or ('evet:' + ssid + "\n" in wifi_list)
    
    # def on_click_continue_button(self, continueButton):
    #     self._screen.show_panel("co_print_chip_selection", "co_print_chip_selection", "Language", 1, False)
    
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)