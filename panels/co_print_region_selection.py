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
#from ks_includes.widgets.timezone import Timezone

# def create_panel(*args):
#     return CoPrintRegionSelection(*args)


# class CoPrintRegionSelection(ScreenPanel):
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        initHeader = InitHeader (self, _('Select Region'),_('Please select your region to determine your time zone.'),'Bolgesecimi')
        self.time_zone_list=[
            {'offset':-12,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-11,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-10,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-9,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-8,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-7,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-6,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-5,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-4,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-3,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-2,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':-1,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':0,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':1,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':2,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':3,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':4,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':5,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':6,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':7,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':8,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':9,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':10,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':11,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':12,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':13,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':14,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None},
            {'offset':15,'timeZoneBox':None,'offset_str':None,'current_time':None,'oset':None}
            ]
        current_time_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        for i, item in enumerate(self.time_zone_list):
            item['oset'] = f"Etc/GMT{'+' if item['offset'] <= 0 else ''}{item['offset']*-1}"
            tz = pytz.FixedOffset(item['offset'] * 60)
            item['current_time']=current_time_utc.astimezone(tz).strftime('%H:%M')
            item['offset_str']=f"GMT{'+' if item['offset'] >= 0 else ''}{item['offset']}"
        
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
        main.pack_start(self.generateTimeZoneGrid(), False, True, 0)
        main.pack_end(buttonBox, False, False, 25)
        
        fixed = Gtk.Overlay()
        fixed.add(image)
        fixed.add_overlay(main)
        self.content.add(fixed)
    
    def timezone_select(self,eventBox, gparam, offset):
       for i, item in enumerate(self.time_zone_list):
            if item['offset']!=offset:
                item['timeZoneBox'].get_style_context().remove_class("timezonebox-active")
            else:
                self.set_timezone(item['oset'])
                self.timeLabel.set_label(item['current_time'])
                item['timeZoneBox'].get_style_context().add_class("timezonebox-active")
    # def timezone_select(self,a,b,c, d):
     
    #    self.set_timezone(c)
    #    self.time_zone_box.get_style_context().add_class("timezone-select-box")
          
    #    self.timeLabel.set_label(d)

    def generateTimeZoneGrid(self):
        timezone_grid = Gtk.Grid()
        timezone_grid.set_halign(Gtk.Align.CENTER)
        timezone_grid.set_row_spacing(20)
        timezone_grid.set_column_spacing(20)
        for i, item in enumerate(self.time_zone_list):
            timezoneLabel = Gtk.Label(item['offset_str'] + " Time Zone", name="timezone-label")
            timezoneLabel.set_justify(Gtk.Justification.LEFT)
            timeLabel = Gtk.Label(item['current_time'], name="time-label")
            timezoneLabel.set_justify(Gtk.Justification.RIGHT)
            timezoneBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            timezoneBox.set_name("timezone-box")
            timezoneBox.pack_start(timezoneLabel, False, False, 0)
            timezoneBox.pack_end(timeLabel, False, False, 0)
            mainEventBox = Gtk.EventBox()
            mainEventBox.add(timezoneBox)
            now = datetime.now()
            if item['current_time'] == now.strftime('%H:%M'):
                item['timeZoneBox'] = Gtk.Frame(name= "timezonebox-active")
            else:
                item['timeZoneBox'] = Gtk.Frame(name= "timezonebox")
            item['timeZoneBox'].add(mainEventBox)
            item['timeZoneBox'].connect("button-press-event", self.timezone_select, item['offset'])
            row = i // 2
            col = i % 2
            timezone_grid.attach(item['timeZoneBox'], col, row, 1, 1)
        self.scroll = self._gtk.ScrolledWindow()
        self.scroll.add(timezone_grid)
        return(self.scroll)
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
        
        self._screen.show_panel(data, data, "Language", 1, True)

    def set_timezone(self, timezone):
        try:
            sudoPassword = self._screen.pc_password
            command = 'timedatectl set-timezone ' + timezone
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            #subprocess.run(["sudo", "timedatectl", "set-timezone", timezone], check=True)
            print(f"Zaman dilimi başarıyla '{timezone}' olarak ayarlandı.")
        except subprocess.CalledProcessError as e:
            print(f"Zaman dilimi ayarlanırken bir hata oluştu: {e}")