import logging
import os
import subprocess
import time
from ks_includes.widgets.areyousuredialog import AreYouSureDialog
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.addnetworkdialog import AddNetworkDialog
from ks_includes.widgets.infodialog import InfoDialog
from ks_includes.widgets.wificard import WifiCard
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintAdvancedSettingScreen(*args)



# class CoPrintAdvancedSettingScreen(ScreenPanel):
class Panel(ScreenPanel):

    def __init__(self, screen, title):
        super().__init__(screen, title)
        box_array = []
        self.open_test = 0
        estimatedMethod = [ { "name":"auto" , "value":"auto" }, { "name":"file", "value":"file" }, { "name":"filament", "value":"filament" }, { "name":"slicer" , "value":"slicer" }]
        fontSize = [ { "name":"small" , "value":"small" }, { "name":"medium", "value":"medium" }, { "name":"large", "value":"large" }]
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
        #
        hourLabel = Gtk.Label(_("24 Hour Time"))
        hourLabelBox = Gtk.EventBox()
        hourLabelBox.add(hourLabel)
        hourLabelBox.connect("button-press-event",self.open_test_screen)
        self.hourSwitch = Gtk.Switch(name = "adv-setting-switch")
        self.hourSwitch.connect("notify::active", self.switch_config_option, 'main', '24htime',None)
        self.hourSwitch.set_active(self._config.get_config().getboolean('main', '24htime'))


        hourBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hourBox.set_name("adv-settings-box-with-switch")
        hourBox.pack_start(hourLabelBox, False, False, 0)
        hourBox.pack_end(self.hourSwitch, False, False, 0)
        box_array.append(hourBox)
        
        #Auto close notifications#
        #
        autoCloseLabel = Gtk.Label(_("Auto close notifications"))
        self.autoCloseSwitch = Gtk.Switch(name = "adv-setting-switch")
        self.autoCloseSwitch.connect("notify::active", self.switch_config_option, 'main', 'autoclose_popups',None)
        self.autoCloseSwitch.set_active(self._config.get_config().getboolean('main', 'autoclose_popups'))
        autoCloseBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        autoCloseBox.set_name("adv-settings-box-with-switch")
        autoCloseBox.pack_start(autoCloseLabel, False, False, 0)
        autoCloseBox.pack_end(self.autoCloseSwitch, False, False, 0)
        #box_array.append(autoCloseBox)
        
        #Confirm emergency stop#
        #
        confirmEmergencyLabel = Gtk.Label(_("Confirm emergency stop"))
        self.confirmEmergencySwitch = Gtk.Switch(name = "adv-setting-switch")
        self.confirmEmergencySwitch.connect("notify::active", self.switch_config_option, 'main', 'confirm_estop',None)
        self.confirmEmergencySwitch.set_active(self._config.get_config().getboolean('main', 'confirm_estop'))
        confirmEmergencyBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        confirmEmergencyBox.set_name("adv-settings-box-with-switch")
        confirmEmergencyBox.pack_start(confirmEmergencyLabel, False, False, 0)
        confirmEmergencyBox.pack_end(self.confirmEmergencySwitch, False, False, 0)
        #box_array.append(confirmEmergencyBox)
        
        #Estimated time method#
        #print_estimate_method
        estimatedTimeLabel = Gtk.Label(_("Estimated time method"))
        estimated_time_store = Gtk.ListStore(str, str)
        estimate_method = self._config.get_config()['main'].get('print_estimate_method', 'auto')
        selected_estimate_index = 0
        for index, estimated in enumerate(estimatedMethod):
            if estimated["value"] == estimate_method:
                selected_estimate_index = index
            estimated_time_store.append([estimated["value"],estimated["name"]])

 
        estimated_time_combo = Gtk.ComboBox.new_with_model(estimated_time_store)
        estimated_time_combo.get_style_context().add_class("adv-setting-combo")
        renderer_text = Gtk.CellRendererText()
        estimated_time_combo.pack_start(renderer_text, True)
        estimated_time_combo.set_column_span_column(1)
        estimated_time_combo.add_attribute(renderer_text, "text", 0)
        estimated_time_combo.connect("changed", self.on_dropdown_change, 'main', 'print_estimate_method', None)
       

        estimated_time_combo.set_active(selected_estimate_index)
        estimatedTimeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        estimatedTimeBox.set_name("adv-settings-box")
        estimatedTimeBox.pack_start(estimatedTimeLabel, False, False, 0)
        estimatedTimeBox.pack_end(estimated_time_combo, False, False, 0)
        #box_array.append(estimatedTimeBox)
        
        #Font Size#
        fontSizeLabel = Gtk.Label(_("Font Size"))
        font_size_store = Gtk.ListStore(str,str)
        
        font_method = self._config.get_config()['main'].get('font_size', 'medium')
        selected_font_index= 0
        for index, font in enumerate(fontSize):
            if font["value"] == font_method:
                selected_font_index = index
            font_size_store.append([font["value"],font["name"]])
            
        font_size_combo = Gtk.ComboBox.new_with_model(font_size_store)
        font_size_combo.get_style_context().add_class("adv-setting-combo")
        font_size_combo.connect("changed", self.on_dropdown_change, 'main', 'font_size', None)
        font_renderer_text = Gtk.CellRendererText()
        font_size_combo.set_column_span_column(1)
        font_size_combo.pack_start(font_renderer_text, True)
        font_size_combo.add_attribute(font_renderer_text, "text", 0)
        font_size_combo.set_active(selected_font_index)
        fontSizeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        fontSizeBox.set_name("adv-settings-box")
        fontSizeBox.pack_start(fontSizeLabel, False, False, 0)
        fontSizeBox.pack_end(font_size_combo, False, False, 0)
        #box_array.append(fontSizeBox)
        
        #Hide sensor in temp#
        #
        hideSensorTempLabel = Gtk.Label(_("Hide sensor in temp"))
        self.hideSensorTempSwitch = Gtk.Switch(name = "adv-setting-switch")

        self.hideSensorTempSwitch.connect("notify::active", self.switch_config_option, 'main', 'only_heaters',None)
        self.hideSensorTempSwitch.set_active(self._config.get_config().getboolean('main', 'only_heaters'))

        hideSensorTempBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hideSensorTempBox.set_name("adv-settings-box-with-switch")
        hideSensorTempBox.pack_start(hideSensorTempLabel, False, False, 0)
        hideSensorTempBox.pack_end(self.hideSensorTempSwitch, False, False, 0)
        #box_array.append(hideSensorTempBox)
        
        #Macro Shortcuts menu#
        #
        macroShortcutLabel = Gtk.Label(_("Macro Shortcuts menu"))
        self.macroShortcutSwitch = Gtk.Switch(name = "adv-setting-switch")

        self.macroShortcutSwitch.connect("notify::active", self.switch_config_option, 'main', 'side_macro_shortcut',None)
        self.macroShortcutSwitch.set_active(self._config.get_config().getboolean('main', 'side_macro_shortcut'))

        macroShortcutBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        macroShortcutBox.set_name("adv-settings-box-with-switch")
        macroShortcutBox.pack_start(macroShortcutLabel, False, False, 0)
        macroShortcutBox.pack_end(self.macroShortcutSwitch, False, False, 0)
        #box_array.append(macroShortcutBox)
        



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
        # settingButton = Gtk.Button(name ="setting-button")
        # settingButton.set_image(settingIcon)
        # settingButton.set_always_show_image(True)
        #settingButton.connect("clicked", self.add_network)




        printerConnectionBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        printerConnectionBox.set_name("adv-settings-box")
        printerConnectionBox.pack_start(printerConnectionLabel, False, False, 0)
        printerConnectionBox.pack_end(settingIcon, False, False, 0)

        printerConnectionEventBox = Gtk.EventBox()
        printerConnectionEventBox.connect("button-press-event", self.change_page)
        printerConnectionEventBox.add(printerConnectionBox)

        box_array.append(printerConnectionEventBox)
        
        #Screen DPMS#
        #
        DPMSLabel = Gtk.Label(_("Screen DPMS"))
        self.DPMSSwitch = Gtk.Switch(name = "adv-setting-switch")

        self.DPMSSwitch.connect("notify::active", self.switch_config_option, 'main', 'use_dpms',None)
        self.DPMSSwitch.set_active(self._config.get_config().getboolean('main', 'use_dpms'))


        DPMSBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        DPMSBox.set_name("adv-settings-box-with-switch")
        DPMSBox.pack_start(DPMSLabel, False, False, 0)
        DPMSBox.pack_end(self.DPMSSwitch, False, False, 0)
        #box_array.append(DPMSBox)
        
        #Screen power off time#
        powerOffTimeLabel = Gtk.Label(_("Screen power off time"))
        power_off_time_store = Gtk.ListStore(str, str)
        # for time in powerOffTime:
        #     power_off_time_store.append([time])

        
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
        
        #Show heater power#
        #
        showHeaterPowerLabel = Gtk.Label(_("Show heater power"))
        self.showHeaterPowerSwitch = Gtk.Switch(name = "adv-setting-switch")

        self.showHeaterPowerSwitch.connect("notify::active", self.switch_config_option, 'main', 'show_heater_power',None)
        self.showHeaterPowerSwitch.set_active(self._config.get_config().getboolean('main', 'show_heater_power'))


        showHeaterPowerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        showHeaterPowerBox.set_name("adv-settings-box-with-switch")
        showHeaterPowerBox.pack_start(showHeaterPowerLabel, False, False, 0)
        showHeaterPowerBox.pack_end(self.showHeaterPowerSwitch, False, False, 0)
        #box_array.append(showHeaterPowerBox)
        
        #Slicer time corrections#
        #print_estimate_compensation

        slicerTimeLabel = Gtk.Label(_("Slicer time corrections (%)"))
        self.scale = Gtk.Scale()
        self.scale.set_range(50, 150)
        scale_value = int(self._config.get_config().get('main', 'print_estimate_compensation', fallback='100'))
        self.scale.set_value(scale_value)
        self.scale.set_increments(1, 1)
        self.scale.set_digits(1)
        self.scale.set_draw_value(True)
        self.scale.set_size_request(-1, 1)
        
        self.scale.connect("button-release-event", self.scale_moved, 'main', 'print_estimate_compensation')
        scaleStyle = self.scale.get_style_context()
        scaleStyle.add_class("slicer-time-scale")
        slicerTimeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=70)
        slicerTimeBox.set_name("adv-settings-box")
        slicerTimeBox.pack_start(slicerTimeLabel, False, False, 0)
        slicerTimeBox.pack_end(self.scale, True, True, 0)
        #box_array.append(slicerTimeBox)
        
        
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
        #main.set_hexpand(True)
       
        main.pack_start(scroll, True, True, 0)
        
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.set_vexpand(True)
        page.pack_start(main, True, True, 0)
        page.pack_end(menu, False, True, 0)
       
        
        self.content.add(page)
    def update_button(self, widget):
        self._screen.show_panel("co_print_system_setting_screen", "co_print_system_setting_screen", "Language", 1, False)

    def change_page(self, widget, event):
        self._screen.show_panel("co_print_printing_brand_selection_new", "co_print_printing_brand_selection_new", "Language", 1, False)
        
    def open_test_screen(self, widget, event):
        self.open_test += 1
        if self.open_test == 3:
            self.open_test = 0
            self._screen.show_panel("co_print_test_screen", "co_print_test_screen", None, 1,False)
        
    def on_scale_changed(self, scale, value):
        
        # Ölçek değeri değiştiğinde çağrılır
        value = int(scale.get_value())
        
        #self.printing.set_fan_speed(self.type,value)
        self.fanSpeedInput.set_text('{:.0f}'.format(value) + '%')
    
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
             
    def changeLang(self, lang):
        self._screen.change_language(lang)
        lang_map = {
            'en': 'en_US.UTF-8',
            'tr': 'tr_TR.UTF-8',
            'fr': 'fr_FR.UTF-8',
            'de': 'de_DE.UTF-8',
            'it': 'it_IT.UTF-8',
            'es': 'es_ES.UTF-8',
        }

        language_map = {
            'en': 'en_US',
            'tr': 'tr_TR',
            'fr': 'fr_FR',
            'de': 'de_DE',
            'it': 'it_IT',
            'es': 'es_ES',
        }

        locale_code = lang_map.get(lang, 'en_US.UTF-8')
        locale_code_language = language_map.get(lang, 'en_US')
       
        sudoPassword = self._screen.pc_password
        command = 'locale-gen ' + locale_code_language
        p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

        command2 = 'update-locale LANG=' + locale_code
        p = os.system('echo %s|sudo -S %s' % (sudoPassword, command2))

        command3 = 'update-locale LC_ALL=' + locale_code
        p = os.system('echo %s|sudo -S %s' % (sudoPassword, command3))
      

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
            self.changeLang(value)
            self._screen.restart_ks()
            print('Ok')
            dialog.destroy()
        

        elif response == Gtk.ResponseType.CANCEL:
            print('Cancel')
            dialog.destroy()
    