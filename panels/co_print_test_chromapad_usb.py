import logging
import os
import pyudev
from gi.repository import Gtk,GLib
from ks_includes.screen_panel import ScreenPanel
from ks_includes.widgets.initheader import InitHeader
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title) 
        initHeader = InitHeader (self, _('USB Test Screen'))
        usbTestLabel = Gtk.Label(_("Connect 3 USBS and Head"), name="usb-yellow-label")
        usbTestLabel.set_halign(Gtk.Align.CENTER)
        usbTestLabel.set_hexpand(Gtk.Align.CENTER)
        self.usbBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.usbBox.pack_start(usbTestLabel, True, True, 10)
        continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        continueButton.connect("clicked", self.on_click_continue_button)
        refreshButton = Gtk.Button(_('Refresh'),name ="flat-button-blue")
        refreshButton.connect("clicked", self.on_click_refreash_button)
        ButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ButtonBox.pack_start(refreshButton, False, False, 0)
        ButtonBox.pack_end(continueButton, False, False, 20)
        self.main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)
        self.main.pack_start(initHeader, True, True, 40)
        self.main.pack_start(self.usbBox, True, True, 40)
        self.main.pack_start(ButtonBox, True, True, 40)
        self.main.set_halign(Gtk.Align.CENTER)
        self.main.set_hexpand(Gtk.Align.CENTER)
        self.content.add(self.main)

    def control_usb(self, args):
        command = 'ls /dev/serial/by-path/*'
        string = os.popen(command).read()
        array = string.split('\n')
        for part in array:
            if part == '':
                array.remove(part)
            logging.info(f"{part}")
        if len(array) == 5:
            for child in self.usbBox.get_children():
                self.usbBox.remove(child)
            twoUsbLabel = Gtk.Label(_("4 USB and Drive Work"), name="usb-green-label")
            twoUsbLabel.set_halign(Gtk.Align.CENTER)
            twoUsbLabel.set_hexpand(Gtk.Align.CENTER)
            self.usbBox.pack_start(twoUsbLabel, True, True, 10)
        if len(array) == 4:
            for child in self.usbBox.get_children():
                self.usbBox.remove(child)
            twoUsbLabel = Gtk.Label(_("3 USB and Drive Work"), name="usb-green-label")
            twoUsbLabel.set_halign(Gtk.Align.CENTER)
            twoUsbLabel.set_hexpand(Gtk.Align.CENTER)
            self.usbBox.pack_start(twoUsbLabel, True, True, 10)
        elif len(array) == 3:
            for child in self.usbBox.get_children():
                self.usbBox.remove(child)
            twoUsbLabel = Gtk.Label(_("2 USB and Drive Work"), name="usb-red-label")
            twoUsbLabel.set_halign(Gtk.Align.CENTER)
            twoUsbLabel.set_hexpand(Gtk.Align.CENTER)
            self.usbBox.pack_start(twoUsbLabel, True, True, 10)
        elif len(array) == 2:
            for child in self.usbBox.get_children():
                self.usbBox.remove(child)
            twoUsbLabel = Gtk.Label(_("1 USB and Drive Work"), name="usb-red-label")
            twoUsbLabel.set_halign(Gtk.Align.CENTER)
            twoUsbLabel.set_hexpand(Gtk.Align.CENTER)
            self.usbBox.pack_start(twoUsbLabel, True, True, 10)
        elif len(array) == 1:
            for child in self.usbBox.get_children():
                self.usbBox.remove(child)
            oneUsbLabel = Gtk.Label(_("Drive Works"), name="usb-red-label")
            oneUsbLabel.set_halign(Gtk.Align.CENTER)
            oneUsbLabel.set_hexpand(Gtk.Align.CENTER)
            self.usbBox.pack_start(oneUsbLabel, True, True, 10)
        elif len(array) == 0: 
            for child in self.usbBox.get_children():
                self.usbBox.remove(child)
            noUsbLabel = Gtk.Label(_("No USB Works"), name="usb-red-label")
            noUsbLabel.set_halign(Gtk.Align.CENTER)
            noUsbLabel.set_hexpand(Gtk.Align.CENTER)
            self.usbBox.pack_start(noUsbLabel, True, True, 10)
        self.content.show_all()

    def on_click_refreash_button(self, continueButton):
        GLib.timeout_add_seconds(1, self.control_usb,None)
    
    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_test_screen", "co_print_test_screen", None, 1,True)
    
    def reinit(self):
        for child in self.usbBox.get_children():
            self.usbBox.remove(child)
        usbTestLabel = Gtk.Label(_("Connect 3 USBS and Head"), name="usb-yellow-label")
        usbTestLabel.set_halign(Gtk.Align.CENTER)
        usbTestLabel.set_hexpand(Gtk.Align.CENTER)
        self.usbBox.pack_start(usbTestLabel, True, True, 10)