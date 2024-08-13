import logging
import os
import subprocess
import time
from ks_includes.widgets.areyousuredialog import AreYouSureDialog
import gi
from ks_includes.widgets.bottommenu import BottomMenu
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):

    def __init__(self, screen, title):
        super().__init__(screen, title)
        box_array = []
        powerOffTime = [{ "name":"300" , "value":"300"}, { "name":"900", "value":"900" }, { "name":"1800", "value":"1800" }, { "name":"3600", "value":"3600" }, 
                        { "name":"7200", "value":"7200" }, { "name":"14400", "value":"14400" }
        ]
        self.languages = [
            {'Lang':'en' ,'Name': _('English'), 'Icon': 'English', 'Button': Gtk.RadioButton()},
            {'Lang':'fr' ,'Name': _('French'), 'Icon': 'France', 'Button': Gtk.RadioButton()},
            {'Lang':'de' ,'Name': _("Deutsch"), 'Icon': 'Germany', 'Button': Gtk.RadioButton()},
            {'Lang':'tr' ,'Name': _("Turkish"), 'Icon': 'Turkey', 'Button': Gtk.RadioButton()},
            {'Lang':'it' ,'Name': _('Italian'), 'Icon': 'Italy', 'Button': Gtk.RadioButton()},
            {'Lang':'es' ,'Name': _('Spanish'), 'Icon': 'Spain', 'Button': Gtk.RadioButton()},
            ]

        self.dialog = None
        menu = BottomMenu(self, False)
        
        #System Update#
        systemLabel = Gtk.Label(_("Systems / Update"))
        systemButton = Gtk.Button(_('Update'),name ="advanced-setting-button")
        systemButton.connect("clicked", self.update_button)
        systemBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        systemBox.set_name("adv-settings-box-with-button")
        systemBox.pack_start(systemLabel, False, False, 0)
        systemBox.pack_end(systemButton, False, False, 0)
        box_array.append(systemBox)
        
        #24 Hour Time#
        hourLabel = Gtk.Label(_("24 Hour Time"))
        self.hourSwitch = Gtk.Switch(name = "adv-setting-switch")
        self.hourSwitch.connect("notify::active", self.switch_config_option, 'main', '24htime',None)
        self.hourSwitch.set_active(self._config.get_config().getboolean('main', '24htime'))
        hourBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hourBox.set_name("adv-settings-box-with-switch")
        hourBox.pack_start(hourLabel, False, False, 0)
        hourBox.pack_end(self.hourSwitch, False, False, 0)
        box_array.append(hourBox)
        
        #Language#
        languageLabel = Gtk.Label(_("Language"))
        language_store = Gtk.ListStore(str, str)
        current_lang_index= 0
        self.current_lang = self._config.current_lang
        for index, language in enumerate(self.languages):
            if language["Lang"] == self.current_lang:
                current_lang_index = index
            language_store.append([language["Name"],language["Lang"]])
        language_combo = Gtk.ComboBox.new_with_model(language_store)
        language_combo.connect("changed", self.on_language_change)
        language_combo.get_style_context().add_class("adv-setting-combo")
        language_renderer_text = Gtk.CellRendererText()
        language_combo.pack_start(language_renderer_text, True)
        language_combo.add_attribute(language_renderer_text, "text", 0)
        language_combo.set_entry_text_column(1)
        language_combo.set_active(current_lang_index)
        languageBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        languageBox.set_name("adv-settings-box")
        languageBox.pack_start(languageLabel, False, False, 0)
        languageBox.pack_end(language_combo, False, False, 0)
        box_array.append(languageBox)
        #Language#      


         #Timezone#
        timezoneLabel = Gtk.Label(_("Country/State"))
        timezone_store = Gtk.ListStore(str, str)
        selected_timezone_index= 0
        current_timezone = time.strftime('%z')
        gmt_offsets = range(-12, 15)
        self.hour_offset = int(current_timezone[:-2])
        for index, offset in enumerate(gmt_offsets):
            if offset == self.hour_offset:
                 selected_timezone_index = index
            oset = f"Etc/GMT{'+' if offset <= 0 else ''}{offset*-1}" 
            offset_str = f"GMT{'+' if offset >= 0 else ''}{offset}"
            timezone_store.append([offset_str,oset])
        timezone_combo = Gtk.ComboBox.new_with_model(timezone_store)
        timezone_combo.connect("changed", self.on_timezone_change)
        timezone_combo.get_style_context().add_class("adv-setting-combo")
        timezone_renderer_text = Gtk.CellRendererText()
        timezone_combo.pack_start(timezone_renderer_text, True)
        timezone_combo.add_attribute(timezone_renderer_text, "text", 0)
        timezone_combo.set_entry_text_column(1)
        timezone_combo.set_active(selected_timezone_index)
        timezoneBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        timezoneBox.set_name("adv-settings-box")
        timezoneBox.pack_start(timezoneLabel, False, False, 0)
        timezoneBox.pack_end(timezone_combo, False, False, 0)
        box_array.append(timezoneBox)
        #timezone#     

        #Printer connections#
        printerConnectionLabel = Gtk.Label(_("Back to Wizard"))
        settingIcon = self._gtk.Image("ayarlar", self._screen.width *.04, self._screen.width *.04)
        printerConnectionBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        printerConnectionBox.set_name("adv-settings-box")
        printerConnectionBox.pack_start(printerConnectionLabel, False, False, 0)
        printerConnectionBox.pack_end(settingIcon, False, False, 0)
        printerConnectionEventBox = Gtk.EventBox()
        printerConnectionEventBox.connect("button-press-event", self.change_page)
        printerConnectionEventBox.add(printerConnectionBox)
        box_array.append(printerConnectionEventBox)
        
        #Screen power off time#
        powerOffTimeLabel = Gtk.Label(_("Screen power off time"))
        power_off_time_store = Gtk.ListStore(str, str)        
        screen_blanking = self._config.get_config()['main'].get('screen_blanking', 'medium')
        screen_blanking_index= 0
        for index, powerOffTime_item in enumerate(powerOffTime):
            if powerOffTime_item["value"] == screen_blanking:
                screen_blanking_index = index
            power_off_time_store.append([powerOffTime_item["value"],powerOffTime_item["name"]])
            
        power_off_time_combo = Gtk.ComboBox.new_with_model(power_off_time_store)
        power_off_time_combo.connect("changed", self.on_dropdown_change, 'main', 'screen_blanking', None)
        power_off_time_combo.get_style_context().add_class("adv-setting-combo")
        power_off_renderer_text = Gtk.CellRendererText()
        power_off_time_combo.pack_start(power_off_renderer_text, True)
        power_off_time_combo.add_attribute(power_off_renderer_text, "text", 0)
        power_off_time_combo.set_entry_text_column(1)
        power_off_time_combo.set_active(screen_blanking_index)
        powerOffTimeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        powerOffTimeBox.set_name("adv-settings-box")
        powerOffTimeBox.pack_start(powerOffTimeLabel, False, False, 0)
        powerOffTimeBox.pack_end(power_off_time_combo, False, False, 0)
        box_array.append(powerOffTimeBox)
        
        scrollBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        for box in box_array:
            scrollBox.pack_start(box, False, False, 0)
            scrollBox.pack_start(Gtk.HSeparator(), False, False, 0)    
        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_kinetic_scrolling(True)
        scroll.get_overlay_scrolling()
        scroll.set_vexpand(True)
        scroll.set_hexpand(True)
        scroll.add(scrollBox)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_name("adv-setting-main-box")
        main.pack_start(scroll, True, True, 0)
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.set_vexpand(True)
        page.pack_start(main, True, True, 0)
        page.pack_end(menu, False, True, 0)
        self.content.add(page)
        
    def update_button(self, widget):
        self._screen.show_panel("co_print_system_setting_screen", "co_print_system_setting_screen", "Language", 1, False)

    def change_page(self, widget, event):
        self._screen.show_panel("co_print_printing_brand_selection_new", "co_print_printing_brand_selection_new", "Language", 1,False)
    
    def on_timezone_change(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            value = model[tree_iter][1]
            self.set_timezone(value)
            logging.debug(f"[]changed to {value}")
            
    
    def on_language_change(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            value = model[tree_iter][1]
            if self.current_lang != value:
                self.open_info_dialog(value)
                logging.debug(f"[]changed to {value}")
            
    def set_timezone(self, timezone):
        try:
            sudoPassword = self._screen.pc_password
            command = 'timedatectl set-timezone ' + timezone
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            #subprocess.run(["sudo", "timedatectl", "set-timezone", timezone], check=True)
            print(f"Zaman dilimi başarıyla '{timezone}' olarak ayarlandı.")
        except subprocess.CalledProcessError as e:
            print(f"Zaman dilimi ayarlanırken bir hata oluştu: {e}")
            
    def open_info_dialog(self,value):
        lang = ""
        for index, language in enumerate(self.languages):
            if value == language['Lang']:
                lang = language['Name']
        content = _("The language will change to " + lang)  
        dialog = AreYouSureDialog( content, self)
        dialog.get_style_context().add_class("network-dialog")
        dialog.set_decorated(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self._screen.change_language(value)
            self._screen.restart_ks()
            print('Ok')
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            print('Cancel')
            dialog.destroy()
    