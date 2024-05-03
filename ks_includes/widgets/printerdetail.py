import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GdkPixbuf, Pango


class PrinterDetail(Gtk.Box):
  

    def __init__(self, this, _printerName, _printerSubName, _printerStatus, _printerStatusStyle, _printerImage):
        super().__init__()
        self.this = this
        self.printerNumber =_printerSubName
        printerDetailBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        printerDetailBox.set_name("printer-detail-box")
        printerDetailBox.set_valign(Gtk.Align.CENTER)
        printerDetailBox.set_halign(Gtk.Align.CENTER)

        
        settingImage = this._gtk.Image("ayarlar", this._screen.width *.025, this._screen.width *.025)
        settingButton = Gtk.Button(name ="printing-stop-button")
        settingButton.set_image(settingImage)
        settingButton.set_always_show_image(True)
        settingButton.set_halign(Gtk.Align.END)
        settingButton.set_valign(Gtk.Align.START)
       # printerDetailBox.pack_start(settingButton, False, False, 0)
        
        
        
        printerName = Gtk.Label('Printer: ' + this._screen.rename_string(_printerName,20), name="printer-name-label")
        
        
        #printerName = Gtk.Label(_printerName, name="printer-name-label")
        
        
        printerNameBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        printerNameBox.pack_start(printerName, False, False, 0)
        printerDetailBox.pack_start(printerNameBox, False, False, 0)
        
        printerSubName = Gtk.Label(this._screen.rename_string(("Printer " + str(_printerSubName)),30), name="printer-sub-name-label")
        printerSubNameBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        printerSubNameBox.pack_start(printerSubName, False, False, 0)
        printerDetailBox.pack_start(printerSubNameBox, False, False, 5)
   
        
        printerStatusLabel = Gtk.Label(_("Printer Status"), name="printer-status-label")
        printerStatus = Gtk.Label("(" + _printerStatus + ")", name =_printerStatusStyle)
        printerStatusBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        printerStatusBox.pack_start(printerStatusLabel, False, False, 0)
        printerStatusBox.pack_start(printerStatus, False, False, 0)
        printerDetailBox.pack_start(printerStatusBox, False, False, 5)
                
        self.detailButton = Gtk.Button(_('Go Printer'),name ="printer-detail-button")
        self.detailButton.connect("clicked", self.connect_printer, _printerName)
        self.detailButton.set_hexpand(False)
        self.detailButton.set_vexpand(False)
        self.detailButton.set_halign(Gtk.Align.START)
        self.detailButton.set_valign(Gtk.Align.START)

        self.setupButton = Gtk.Button(_('Setup Printer'),name ="printer-setup-button")
        self.setupButton.connect("clicked", self.setup_printer)
        self.setupButton.set_hexpand(False)
        self.setupButton.set_vexpand(False)
        self.setupButton.set_halign(Gtk.Align.START)
        self.setupButton.set_valign(Gtk.Align.START)



        if _printerStatusStyle == 'printer-status-not-configured':
            printerDetailBox.pack_end(self.setupButton, False, False, 10)
        else:
            printerDetailBox.pack_end(self.detailButton, False, False, 10)
        
        
        printerImage = this._gtk.Image(_printerImage, this._screen.width *.15, this._screen.width *.15)
        printerBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        printerBox.set_halign(Gtk.Align.CENTER)
        printerBox.set_valign(Gtk.Align.CENTER)
        printerBox.pack_start(printerImage, False, False, 0)
    
        
        changePrinterBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        

        changePrinterBox.pack_start(printerBox, False, False, 0)
        changePrinterBox.pack_start(printerDetailBox, False, False, 0)
        
            
        settingButtonWithChangePrinterBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        settingButtonWithChangePrinterBox.set_name("change-printer-box")
        settingButtonWithChangePrinterBox.pack_start(settingButton, False, False, 0)
        settingButtonWithChangePrinterBox.pack_start(changePrinterBox, False, False, 0)
        
        
       
        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main.set_halign(Gtk.Align.CENTER)
        main.set_valign(Gtk.Align.CENTER)
        main.pack_start(settingButtonWithChangePrinterBox, False, False, 0)

        self.add(main)

    def connect_printer(self, widget, name):
        self.this._screen.connect_printer(name)

    def setup_printer(self, widget):
        print(self.printerNumber)
        self.this._screen.selected_wizard_printer = 'Printer'+str(self.printerNumber)+'WizardDone'
        self.this._screen.selected_printer_index = self.printerNumber
        self.this._screen.show_panel("co_print_printing_brand_selection_new", "co_print_printing_brand_selection_new", "Language", 1, False)

    