import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GdkPixbuf


class BottomMenu(Gtk.Box):
  

    def __init__(self, this, _backButtonActive):
        super().__init__()
        
        menuBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        menuBox.set_name("bottom-menu-box")
        self.parent = this
        dashboardIcon = this._gtk.Image("dashboard", 35, 35)
        printFilesIcon = this._gtk.Image("folder", 35, 35)
        printersIcon = this._gtk.Image("printerchange", 35, 35)
        configureIcon = this._gtk.Image("configure", 35, 35)
        emergencyStopIcon = this._gtk.Image("emergencyicon", 35, 35)
        refreshIcon = this._gtk.Image("update", 35, 35)
        backIcon = this._gtk.Image("back-arrow", 35, 35)
        
        # if _backButtonActive:
        #     backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        #     backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        #     backButtonBox.set_halign(Gtk.Align.CENTER)
        #     backButtonBox.set_valign(Gtk.Align.CENTER)
        #     backButtonBox.pack_start(backIcon, False, False, 0)
        #     backButtonBox.pack_start(backLabel, False, False, 0)
        #     self.backButton = Gtk.Button(name ="menu-buttons")
        #     self.backButton.add(backButtonBox)
        #     self.backButton.connect("clicked", self.on_click_menu_button, 'co_print_home_screen')
        #     self.backButton.set_always_show_image (True)
        #     menuBox.pack_start(self.backButton, True, True, 0)
        # else:
        dashboardLabel = Gtk.Label(("Dashboard"), name="bottom-menu-label")            
        dashboardButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        dashboardButtonBox.set_halign(Gtk.Align.CENTER)
        dashboardButtonBox.set_valign(Gtk.Align.CENTER)
        dashboardButtonBox.pack_start(dashboardIcon, False, False, 0)
        dashboardButtonBox.pack_start(dashboardLabel, False, False, 0)
        self.dashboardButton = Gtk.Button(name ="menu-buttons")
        self.dashboardButton.add(dashboardButtonBox)
        self.dashboardButton.connect("clicked", self.on_click_menu_button, 'co_print_home_screen')
        self.dashboardButton.set_always_show_image (True)
        menuBox.pack_start(self.dashboardButton, True, True, 0)
            
         
        printFilesLabel = Gtk.Label(("Print Files"), name="bottom-menu-label")            
        printFilesButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        printFilesButtonBox.set_halign(Gtk.Align.CENTER)
        printFilesButtonBox.set_valign(Gtk.Align.CENTER)
        printFilesButtonBox.pack_start(printFilesIcon, False, False, 0)
        printFilesButtonBox.pack_start(printFilesLabel, False, False, 0)
        printFilesButton = Gtk.Button(name ="menu-buttons")
        printFilesButton.add(printFilesButtonBox)
        printFilesButton.connect("clicked", self.on_click_menu_button, 'co_print_printing_files_screen', False)
        printFilesButton.set_always_show_image (True)
        menuBox.pack_start(printFilesButton, True, True, 0)
            
        pintersLabel = Gtk.Label(("Printers"), name="bottom-menu-label")            
        pintersButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        pintersButtonBox.set_halign(Gtk.Align.CENTER)
        pintersButtonBox.set_valign(Gtk.Align.CENTER)
        pintersButtonBox.pack_start(printersIcon, False, False, 0)
        pintersButtonBox.pack_start(pintersLabel, False, False, 0)
        pintersButton = Gtk.Button(name ="menu-buttons")
        pintersButton.add(pintersButtonBox)
        pintersButton.connect("clicked", self.on_click_menu_button, 'co_print_change_printer', False)
        pintersButton.set_always_show_image (True)
        menuBox.pack_start(pintersButton, True, True, 0)

        configureLabel = Gtk.Label(("Configure"), name="bottom-menu-label")            
        configureButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        configureButtonBox.set_halign(Gtk.Align.CENTER)
        configureButtonBox.set_valign(Gtk.Align.CENTER)
        configureButtonBox.pack_start(configureIcon, False, False, 0)
        configureButtonBox.pack_start(configureLabel, False, False, 0)
        configureButton = Gtk.Button(name ="menu-buttons")
        configureButton.add(configureButtonBox)
        configureButton.connect("clicked", self.on_click_menu_button, 'co_print_setting_screen', False)
        configureButton.set_always_show_image (True)
        menuBox.pack_start(configureButton, True, True, 0)
        
        emergencyStopButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        emergencyStopButtonBox.set_halign(Gtk.Align.CENTER)
        emergencyStopButtonBox.set_valign(Gtk.Align.CENTER)
        emergencyStopButtonBox.pack_start(emergencyStopIcon, False, False, 0)
        emergencyStopButton = Gtk.Button(name ="emergency-button")
        emergencyStopButton.add(emergencyStopButtonBox)
        emergencyStopButton.connect("clicked", self.on_click_emergency_stop)
        emergencyStopButton.set_always_show_image (True)
        menuBox.pack_start(emergencyStopButton, True, False, 0)
        
        restartServiceButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        restartServiceButtonBox.set_halign(Gtk.Align.CENTER)
        restartServiceButtonBox.set_valign(Gtk.Align.CENTER)
        restartServiceButtonBox.pack_start(refreshIcon, False, False, 0)
        restartServiceButton = Gtk.Button(name ="emergency-button")
        restartServiceButton.add(restartServiceButtonBox)
        restartServiceButton.connect("clicked", this._screen.restart_ks)
        restartServiceButton.set_always_show_image (True)
        #menuBox.pack_start(restartServiceButton, True, False, 0)
        
        menuBox.set_hexpand(True)
        self.add(menuBox)

    def on_click_emergency_stop(self, button):
        self.parent._screen._ws.klippy.emergency_stop()

    def on_click_menu_button(self, button, data, active_page = True):
        if  active_page:
            if self.parent._printer.state == 'error' or self.parent._printer.state == 'shutdown' or self.parent._printer.state == 'disconnected':
                self.parent._screen.show_panel("co_print_home_not_connected_screen", "co_print_home_not_connected_screen",
                                        "Language", 1, True)
            else:
                self.parent._screen.show_panel(data, data, "Language", 1, True)
        elif data == 'co_print_printing_files_screen' and  (self.parent._printer.state == 'printing' or self.parent._printer.state == 'paused'):
            self.parent._screen.show_panel('co_print_printing_screen', 'co_print_printing_screen', "Language", 1, False)
        elif(self.parent._printer.state != 'printing'):
            self.parent._screen.show_panel(data, data, "Language", 1, False)