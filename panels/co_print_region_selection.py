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
from ks_includes.widgets.timezone import Timezone

# def create_panel(*args):
#     return CoPrintRegionSelection(*args)


# class CoPrintRegionSelection(ScreenPanel):
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        initHeader = InitHeader (self, _('Select Region'),_('Please select your region to determine your time zone.'),'Bolgesecimi')


        


        current_time_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        gmt_offsets = range(-12, 15)
        times_in_timezones = []
        for offset in gmt_offsets:
            oset = f"Etc/GMT{'+' if offset <= 0 else ''}{offset*-1}"
            tz = pytz.FixedOffset(offset * 60)
            current_time_in_tz = current_time_utc.astimezone(tz)
            offset_str = f"GMT{'+' if offset >= 0 else ''}{offset}"
            times_in_timezones.append((offset_str, current_time_in_tz.strftime('%H:%M'), oset))

        timezone_grid = Gtk.Grid()
        timezone_grid.set_halign(Gtk.Align.CENTER)
        timezone_grid.set_row_spacing(20)
        timezone_grid.set_column_spacing(20)
        
        for index, (offset, current_time, oset) in enumerate(times_in_timezones):
            self.time_zone_box = Timezone(self, offset, current_time, oset)
            row = index // 2
            col = index % 2
            timezone_grid.attach(self.time_zone_box, col, row, 1, 1)
           
        self.scroll = self._gtk.ScrolledWindow()
        self.scroll.add(timezone_grid)
        now = datetime.now()        
             
        currentLabel = Gtk.Label("Current: ", name="current-time-label")
        self.timeLabel = Gtk.Label(now.strftime('%H:%M')  , name="current-time-label")
        currentTimeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        currentTimeBox.set_halign(Gtk.Align.CENTER)
        currentTimeBox.pack_start(currentLabel, False, False, 0)
        currentTimeBox.pack_start(self.timeLabel, False, False, 0)



        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.pack_start(self.continueButton, False, False, 0)
        buttonBox.set_center_widget(self.continueButton)
   
        
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
        
        image = self._gtk.Image("Wordmapdots", self._gtk.content_width * 1.1 , self._gtk.content_height * 1.1)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        main.set_hexpand(True)
        main.set_vexpand(True)
        main.pack_start(mainBackButtonBox, False, False, 0)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(currentTimeBox, False, False, 13)
        main.pack_start(self.scroll, False, True, 0)
        main.pack_end(buttonBox, False, False, 25)
        
        
        fixed = Gtk.Overlay()
        fixed.add(image)
        fixed.add_overlay(main)
        self.content.add(fixed)

    def timezone_select(self,a,b,c, d):
     
       self.set_timezone(c)
       self.time_zone_box.get_style_context().add_class("timezone-select-box")
          
       self.timeLabel.set_label(d)

        
    # def on_country_combo_changed(self, combo):
    #     tree_iter = combo.get_active_iter()
    #     if tree_iter is not None:
    #         model = combo.get_model()
    #         country = model[tree_iter][0]
    #         print("Selected: country=%s" % country)

    # def change_timezone(self, timezone):
    #     command = f"timedatectl set-timezone {timezone.get_text()}"
    #     subprocess.run(command, shell=True)

    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_product_naming", "co_print_product_naming", None, 1,False)
        
    # def on_combobox_changed(self, combobox):
    #     active_text = combobox.get_active_text()
    #     print("Seçilen seçenek:", active_text)
        
    # def on_listbox_row_activated(self, listbox, row):
    #     selected_value = row.get_child().get_label()
    #     self.entry.set_text(selected_value)
        
    # def on_arrow_clicked(self, widget, event):
    #     if self.listbox.get_visible():
    #         self.listbox.hide()
    #     else:
    #         allocation = self.entry.get_allocation()
    #         x, y = self.entry.translate_coordinates(self, allocation.x, allocation.y + allocation.height)
    #         self.listbox.set_size_request(allocation.width, -1)
    #         self.move(x, y)
    #         self.listbox.show_all()
    # def on_button_clicked(self, button):
    #     if self.listbox.get_visible():
    #         self.listbox.hide()
    #     else:
    #         self.listbox.show()
    
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, False)

    def set_timezone(self, timezone):
        try:
            sudoPassword = self._screen.pc_password
            command = 'timedatectl set-timezone ' + timezone
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            #subprocess.run(["sudo", "timedatectl", "set-timezone", timezone], check=True)
            print(f"Zaman dilimi başarıyla '{timezone}' olarak ayarlandı.")
        except subprocess.CalledProcessError as e:
            print(f"Zaman dilimi ayarlanırken bir hata oluştu: {e}")