import logging
import os
import socket
import numpy as np
import subprocess
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.addnetworkdialog import AddNetworkDialog
from ks_includes.widgets.infodialog import InfoDialog
from ks_includes.widgets.wificard import WifiCard
import netifaces
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintNetworkSettingScreen(*args)


class CoPrintNetworkSettingScreen(ScreenPanel):


    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        menu = BottomMenu(self, False)
        self.ip = '--'
        connectionSettingsLabel = Gtk.Label(_("Connection Settings"), name="connection-setting-label")
        connectionSettingsLabel.set_justify(Gtk.Justification.LEFT)
        connectionSettingsLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        connectionSettingsLabelBox.pack_start(connectionSettingsLabel, False, False, 0)
        
        self.IpLabel = Gtk.Label(_("IP") + ":" + self.ip, name="ip-label")
        self.IpLabel.set_justify(Gtk.Justification.LEFT)
        IpLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        IpLabelBox.pack_start(self.IpLabel, False, False, 0)

        refreshIcon = self._gtk.Image("update", self._screen.width *.028, self._screen.width *.028)
        refreshButton = Gtk.Button(name ="setting-button")
        refreshButton.connect("clicked", self.refresh)
        refreshButton.set_image(refreshIcon)
        refreshButton.set_always_show_image(True)
        refreshButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        refreshButtonBox.set_valign(Gtk.Align.CENTER)
        refreshButtonBox.add(refreshButton)
        
        connectionSettingLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        connectionSettingLabelBox.pack_start(connectionSettingsLabelBox, False, False, 0)
        connectionSettingLabelBox.pack_start(refreshButtonBox, False, False, 0)
        
        connectionSettingsBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        connectionSettingsBox.pack_start(connectionSettingLabelBox, False, False, 0)
        connectionSettingsBox.pack_start(IpLabelBox, False, False, 0)
        
        
        self.addNetworkButton = Gtk.Button(_('Add Network'),name ="add-network-button")
        self.addNetworkButton.connect("clicked", self.add_network, '')
        addNetworkButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        addNetworkButtonBox.set_valign(Gtk.Align.CENTER)
        addNetworkButtonBox.pack_start(self.addNetworkButton, False, False, 0)
        
        connectionBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        connectionBox.set_valign(Gtk.Align.CENTER)
        connectionBox.set_name("connection-box")
        connectionBox.set_hexpand(True)
        connectionBox.pack_start(connectionSettingsBox, False, False, 0)
        connectionBox.pack_end(addNetworkButtonBox, False, False, 0)
        
        GLib.idle_add(self.refresh, None)  
    #     wifione = WifiCard(self, "signal-high", "Co Print 5G", ("Connected"))
    #     wifitwo = WifiCard(self, "signal-high", "TurkTelekom Wifi", ("Click to connect."))
    #     wifithree = WifiCard(self, "signal-medium", "Superonline Wifi", ("Click to connect."))
    #     wififour = WifiCard(self, "signal-medium", "Superonline Wifi", ("Click to connect."))
    #     wififive = WifiCard(self, "signal-medium", "Superonline Wifi", ("Click to connect."))
    #     wifisix = WifiCard(self, "signal-low", "Superonline Wifi2", ("Click to connect."))
    #     wifiseven = WifiCard(self, "signal-low", "Superonline Wifi2", ("Click to connect."))

        wifi_flowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        wifi_flowbox.set_halign(Gtk.Align.CENTER)
        wifi_flowbox.set_hexpand(True)
    #    # wifi_flowbox.set_hexpand(True)
        
    #     wifi_flowbox.pack_start(wifione, True, True, 0)
    #     wifi_flowbox.pack_start(wifitwo, True, True, 10)
    #     wifi_flowbox.pack_start(wifithree, True, True, 0)
    #     wifi_flowbox.pack_start(wififour, True, True, 10)
    #     wifi_flowbox.pack_start(wififive, True, True, 0)
    #     wifi_flowbox.pack_start(wifisix, True, True, 10)
    #     wifi_flowbox.pack_start(wifiseven, True, True, 10)
    
        spinner = Gtk.Spinner()
        spinner.props.width_request = 100  
        spinner.props.height_request = 100
        spinner.start()
     
        self.scroll = self._gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_kinetic_scrolling(True)
        self.scroll.get_overlay_scrolling()
        self.scroll.add(spinner)
        self.scrolBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.scrolBox.pack_start(self.scroll, True, True, 0)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(connectionBox, False, False, 0)
        main.pack_start(self.scrolBox, False, True, 50)
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(main, True, True, 0)
        page.pack_end(menu, False, True, 0)
        
        self.content.add(page)

    def add_network(self, widget, name):
        
        dialog = AddNetworkDialog( name, self)
        dialog.get_style_context().add_class("network-dialog")
        dialog.set_decorated(False)

        response = dialog.run()
 
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
            psw = dialog.psw
            ssid = dialog.ssid
            command = ["nmcli", "device", "wifi", "connect", ssid, "password", psw]
            #self.execute_command_and_show_output(command, ssid, psw)


            GLib.idle_add(self.execute_command_and_show_output, command, ssid, psw)  
            self.waitDialog = InfoDialog(self, _("Please Wait"), True)
            self.waitDialog.get_style_context().add_class("alert-info-dialog")

            self.waitDialog.set_decorated(False)
            self.waitDialog.set_size_request(0, 0)
            response = self.waitDialog.run()


            
        elif response == Gtk.ResponseType.CANCEL:
            subprocess.Popen(["pkill", "onboard"])
            dialog.destroy()
    
    def refresh(self, widget):

        gws = netifaces.gateways()
        if "default" in gws and netifaces.AF_INET in gws["default"]:
            self.interface = gws["default"][netifaces.AF_INET][1]
        else:
            ints = netifaces.interfaces()
            if 'lo' in ints:
                ints.pop(ints.index('lo'))
            if len(ints) > 0:
                self.interface = ints[0]
            else:
                self.interface = 'lo'

        ifadd = netifaces.ifaddresses(self.interface)
        if netifaces.AF_INET in ifadd and len(ifadd[netifaces.AF_INET]) > 0:
            ipv4 =  f"{ifadd[netifaces.AF_INET][0]['addr']}"

            #ip = host_addr
            self.IpLabel.set_label(_("IP") + ":" + ipv4)

        spinner = Gtk.Spinner()
        spinner.props.width_request = 100  
        spinner.props.height_request = 100
        spinner.start()
        for child in self.scroll.get_children():
                self.scroll.remove(child)
        self.scroll.add(spinner)
        self.content.show_all()        
        


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
                if(len(wifiarray)> 0):
                    bar = wifiarray.pop()
                    name = ' '.join(wifiarray)
                    if(str(name)!= "SSID" and str(name) != "--"):
                        icon = 'signal-low'
                        if(len(bar) == 4):
                            icon = 'signal-high'
                        if(len(bar) == 3):
                            icon = 'signal-medium'
                        if str(name) not in wifiNames:
                            wifiNames.append(str(name))
                            connectionStatus = self.is_connected_to(str(name), connected_wifi_list)
                            if connectionStatus:
                                self.wifies.insert(0, {'Name': str(name), 'Icon': icon, 'ConnectionStatus': connectionStatus})
                            else:    
                                self.wifies.append({'Name': str(name), 'Icon': icon, 'ConnectionStatus': connectionStatus})


            for wifi in self.wifies:
                connection_button_visible = False  
                connection_status = _('Not Connected')
                if wifi['ConnectionStatus']:
                    connection_status = _('Connected')
                    connection_button_visible = True
                 
                wifione = WifiCard(self, wifi['Icon'], wifi['Name'], connection_status, connection_button_visible)
               
                wifi_flowbox.pack_start(wifione, False, False, 0)
               

            for child in self.scroll.get_children():
                self.scroll.remove(child)
        else:

            wifione = WifiCard(self, "signal-high", "Co Print 5Gadasdasdasdasdasd", "Connected", True)
            wifitwo = WifiCard(self, "signal-high", "TurkTelekom Wifi", "Click to connect.", False)
            wifithree = WifiCard(self, "signal-medium", "Superonline Wifi", "Click to connect.", False)
            wififour = WifiCard(self, "signal-medium", "Superonline Wifi", "Click to connect.", False)
            wififive = WifiCard(self, "signal-medium", "Superonline Wifi", "Click to connect.", False)
            wifisix = WifiCard(self, "signal-low", "Superonline Wifi2", "Click to connect.", False)
            wifiseven = WifiCard(self, "signal-low", "Superonline Wifi2", "Click to connect.", False)
            wifi_flowbox.pack_start(wifione, True, True, 0)
            wifi_flowbox.pack_start(wifitwo, True, True, 0)
            wifi_flowbox.pack_start(wifithree, True, True, 0)
            wifi_flowbox.pack_start(wififour, True, True, 0)
            wifi_flowbox.pack_start(wififive, True, True, 0)
            wifi_flowbox.pack_start(wifisix, True, True, 0)
            wifi_flowbox.pack_start(wifiseven, True, True, 0)
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
        return ('yes:'+ ssid +"\n" in  wifi_list ) or ('evet:'+ ssid +"\n" in  wifi_list )
    
    def wifiChanged(self,widget , event, name):
      
       self.add_network(None, name)
    
    def execute_command_and_show_output(self, command, name, psw):
        try:
            status = self.connect_to(name, psw)
            
            if status:
                self.close_dialog(self.waitDialog)
                self._screen.show_panel("co_print_home_screen", "co_print_home_screen", None, 2, True, items=name, password=psw)
            else:
                self.close_dialog(self.waitDialog)
                self.showMessageBox(_('Connection Failed'))

            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            ip = IPAddr
            self.IpLabel.set_label(_("IP") + ":" + ip)
           
           
        except subprocess.CalledProcessError as e:
            self.showMessageBox(e.output.decode("utf-8"))

    def showMessageBox(self, message):
        self.dialog = InfoDialog(self, message, True)
        self.dialog.get_style_context().add_class("alert-info-dialog")

        self.dialog.set_decorated(False)
        self.dialog.set_size_request(0, 0)
        timer_duration = 3000
        GLib.timeout_add(timer_duration, self.close_dialog, self.dialog)
        response = self.dialog.run()
    
    def connect_to(self, ssid: str, password: str):
        wifi_list_string = subprocess.check_output(['nmcli', '-f', 'NAME', 'con', 'show']).decode()
        wifi_list = wifi_list_string.split("\n")
        is_saved = np.any([ssid in i.strip() for i in wifi_list])

        if is_saved:
            subprocess.call(['nmcli', 'c', 'up', 'id', ssid])
        else:
            subprocess.call(['nmcli', 'd', 'wifi', 'connect', ssid, 'password', password])
        connected_wifi_list = self.what_wifi()
        return self.is_connected_to(ssid, connected_wifi_list)
    
    def close_dialog(self, dialog):
        dialog.response(Gtk.ResponseType.CANCEL)
        dialog.destroy()  