import logging
import os
import pytz
import subprocess
from datetime import datetime

import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintRegionSelection(*args)


class CoPrintRegionSelection(ScreenPanel):

    def __init__(self, screen, title):
        super().__init__(screen, title)
        initHeader = InitHeader (self, _('Select Region'),_('Please select your region to determine your time zone.'),'Bolgesecimi')
        countries = []
        timezones = pytz.all_timezones
        for timezone in timezones:
           countries.append(timezone)
         
        # Şu anki UTC saatini alalım
        current_time_utc = datetime.utcnow()

        # GMT ofsetleri listesini oluşturalım
        gmt_offsets = range(-12, 15)

        # GMT ofsetleri için zamanları saklayacak bir liste oluşturalım
        times_in_timezones = []

        # Tüm GMT ofsetlerinde gezelim
        for offset in gmt_offsets:
            tz_name = f"Etc/GMT{'+' if offset < 0 else '-'}{abs(offset)}" if offset != 0 else "Etc/GMT"
            tz = pytz.timezone(tz_name)
            current_time_in_tz = current_time_utc.astimezone(tz)
            offset_str = f"GMT{'+' if offset >= 0 else ''}{offset:02d}"
            times_in_timezones.append((offset_str, current_time_in_tz.strftime('%Y-%m-%d %H:%M:%S')))

        # Sonuçları yazdıralım
        
        printer_grid = Gtk.Grid()
        printer_grid.set_row_spacing(20)
        printer_grid.set_column_spacing(20)
        left = 0
        top = 0
        for offset, current_time in times_in_timezones:
            #print(f"{offset}: {current_time}")
            time_zone_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            offset_label = Gtk.Label(label=offset, xalign=0, name="region-menu-label")
            time_label = Gtk.Label(label=current_time, xalign=0, name="region-menu-label")
            printingDetail = time_zone_box
            printer_grid.attach(printingDetail, left, top, 1, 1)
            if left == 0:
                left = 1
            else:
                left = 0
                top += 1


        



        # ComboBox'u oluştur
        self.regionCombobox = Gtk.ComboBoxText.new_with_entry()
        self.regionCombobox.set_name("region-combobox")
        self.regionCombobox.set_entry_text_column(0)
        self.regionCombobox.connect("changed", self.on_combobox_changed)
     
        # Entry'ı oluştur
        self.entry = Gtk.Label(xalign=0, name="region-menu-label")
        #self.entry.set_margin_left(20) 
        self.entry.get_style_context().add_class("region-entry")
        #self.entry.set_editable(False)
        #self.entry.set_can_focus(False)

        self.regionCombobox.set_active(0)

        # Açılır listenin boyutunu ayarla
        combo_box_text = self.regionCombobox.get_child()
        style_context = combo_box_text.get_style_context()
        style_context.add_class("custom-region")
       
        self.listbox = Gtk.ListBox(name ="region")
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        
        for country in countries:
            label = Gtk.Label(label=country, xalign=0, name="region-menu-label")
            label.set_name("region-label")
            label.set_margin_left(20) 
            label.set_justify(Gtk.Justification.LEFT) 
            self.listbox.add(label)

        
        self.listbox.set_activate_on_single_click(True)
        self.listbox.connect("row-activated", self.on_listbox_row_activated)
        
        self.scroll = self._gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_kinetic_scrolling(True)
        self.scroll.get_overlay_scrolling()
      
        self.scroll.add(printer_grid)
        
        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.pack_start(self.continueButton, False, False, 0)
        buttonBox.set_center_widget(self.continueButton)
   
        
        self.listOpenButton = Gtk.Button(image=self._gtk.Image("expand-arrow-down", 50, 50), name ="region-combobox-button")
        self.listOpenButton.connect("clicked", self.on_button_clicked)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        vbox.pack_start(self.entry, True, True, 0)
        vbox.pack_end(self.listOpenButton, False, False, 0)
        
        vbox_with_comboBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox_with_comboBox.set_halign(Gtk.Align.CENTER)
        vbox_with_comboBox.pack_start(vbox, False, False, 0)
        vbox_with_comboBox.pack_start(printer_grid, False, True, 0)
        vbox_with_comboBox.set_name("region-select-box")
        
        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_contract_approval')
        self.backButton.set_always_show_image (True)       
        mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainBackButtonBox.pack_start(self.backButton, False, False, 0)
        
        image = self._gtk.Image("Wordmapdots", self._gtk.content_width * 1.1 , self._gtk.content_height * 1.1)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        main.set_hexpand(True)
        main.set_vexpand(True)
        #main.set_halign(Gtk.Align.CENTER)
        main.pack_start(mainBackButtonBox, False, False, 0)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(vbox_with_comboBox, False, True, 0)
        main.pack_end(buttonBox, True, False, 5)
        
        
        fixed = Gtk.Overlay()
        fixed.add(image)
        fixed.add_overlay(main)
        self.content.add(fixed)

        
    def on_country_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            country = model[tree_iter][0]
            print("Selected: country=%s" % country)

    def change_timezone(self, timezone):
        command = f"timedatectl set-timezone {timezone.get_text()}"
        subprocess.run(command, shell=True)

    def on_click_continue_button(self, continueButton):
        self.change_timezone(self.entry)
        self._screen.show_panel("co_print_product_naming", "co_print_product_naming", None, 2)
        
    def on_combobox_changed(self, combobox):
        active_text = combobox.get_active_text()
        print("Seçilen seçenek:", active_text)
        
    def on_listbox_row_activated(self, listbox, row):
        # Seçilen öğenin değerini Entry kutusuna yazdırma
        selected_value = row.get_child().get_label()
        self.entry.set_text(selected_value)
        
    def on_arrow_clicked(self, widget, event):
        # Ok simgesi tıklandığında yapılacak işlemler
        if self.listbox.get_visible():
            self.listbox.hide()
        else:
            allocation = self.entry.get_allocation()
            x, y = self.entry.translate_coordinates(self, allocation.x, allocation.y + allocation.height)
            self.listbox.set_size_request(allocation.width, -1)
            self.move(x, y)
            self.listbox.show_all()
    def on_button_clicked(self, button):
        # Listbox öğesinin görünürlüğünü tersine çevirme
        if self.listbox.get_visible():
            self.listbox.hide()
        else:
            self.listbox.show()
    
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, False)