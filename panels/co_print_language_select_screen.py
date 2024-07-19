import logging
import os
import subprocess
import sys
import locale
import gi
from ks_includes.widgets.infodialog import InfoDialog

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk

from ks_includes.screen_panel import ScreenPanel
import gettext
# def create_panel(*args):
#     return CoPrintSplashScreenPanel(*args)


# class CoPrintSplashScreenPanel(ScreenPanel):

class Panel(ScreenPanel):     
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.languages = [
            {'Lang':'en' ,'Name': _('English'), 'Icon': 'English', 'Button': Gtk.RadioButton()},
            {'Lang':'fr' ,'Name': _('French'), 'Icon': 'France', 'Button': Gtk.RadioButton()},
            {'Lang':'de' ,'Name': _("Deutsch"), 'Icon': 'Germany', 'Button': Gtk.RadioButton()},
            {'Lang':'tr' ,'Name': _("Turkish"), 'Icon': 'Turkey', 'Button': Gtk.RadioButton()},
            {'Lang':'it' ,'Name': _('Italian'), 'Icon': 'Italy', 'Button': Gtk.RadioButton()},
            {'Lang':'es' ,'Name': _('Spanish'), 'Icon': 'Spain', 'Button': Gtk.RadioButton()},
            
            ]
        self.lang_changed = False
        self.labels['actions'] = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.labels['actions'].set_hexpand(True)
        self.labels['actions'].set_vexpand(False)
        self.labels['actions'].set_halign(Gtk.Align.CENTER)
        self.labels['actions'].set_homogeneous(True)
        self.labels['actions'].set_size_request(self._gtk.content_width, -1)

       
        initHeader = InitHeader (self, _('Language Settings'), _('Please specify the system language'), "Geography")

        '''diller'''
        grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=10,
                         row_spacing=10)
        row = 0
        count = 0
        #group =  [x for x in languages if x['Lang'] == i18n.get('locale')][0]['Button']
        self.group =  self.languages[0]['Button']
        self.new_lang = None
        self.current_lang =  self._config.current_lang
        for language in self.languages:
            
            languageImage = self._gtk.Image(language['Icon'], self._gtk.content_width * .05 , self._gtk.content_height * .05)
            languageName = Gtk.Label(language['Name'],name ="language-label")
            language['Button'] = Gtk.RadioButton.new_with_label_from_widget(self.group,"")
            
            if self.current_lang == language['Lang']:
                language['Button'].set_active(True)
            language['Button'].connect("toggled",self.radioButtonSelected, language['Lang'])
            
             
            languageBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            f = Gtk.Frame()
            languageBox.pack_start(languageImage, False, True, 5)
            languageBox.pack_end(language['Button'], False, False, 5)
            languageBox.pack_end(languageName, True, True, 5)
            languageBox.set_size_request(50, 50)

            eventBox = Gtk.EventBox()
            eventBox.connect("button-press-event", self.eventBoxLanguage, language['Lang'])
            eventBox.add(languageBox)


            f.add(eventBox)
            grid.attach(f, count, row, 1, 1)
            count += 1
            if count % 2 == 0:
                count = 0
                row += 1


       
        
        gridBox = Gtk.Box()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)
        '''diller bitis'''
        
        
        
        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        
        self.continueButton.set_hexpand(True)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.pack_start(self.continueButton, False, False, 0)
       
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.pack_start(initHeader, True, True, 0)
        main.pack_end(buttonBox, True, True, 20)
        main.pack_end(gridBox, True, True, 20)
        
        self.show_restart_buttons()
      
        self.content.add(main)
        self._screen.base_panel.visible_menu(False)
       
    def on_click_continue_button(self, continueButton):
        if self.lang_changed:
            self.changeLang(self.new_lang)
            self._screen.restart_ks()
        else:
            self._screen.show_panel("co_print_contract_approval", "co_print_contract_approval", None, 1, True)

    def changeLang(self, lang):
        if lang != self.current_lang:
            self.lang_changed = True
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


    def radioButtonSelected(self, button, lang):
        if lang != self.current_lang: 
            self.new_lang = lang
            self.lang_changed = True
        else:
            self.lang_changed = False
    
    def eventBoxLanguage(self, button, gparam, lang):
            for language in self.languages:
                if lang != language['Lang']:
                    language['Button'].set_active(False)
                else:
                    language['Button'].set_active(True)


    def _resolve_radio(self, master_radio):
        active = next((
        radio for radio in
        master_radio.get_group()
        if radio.get_active()
        ))
        return active

    def update_text(self, text):
        
        self.show_restart_buttons()

    def clear_action_bar(self):
        for child in self.labels['actions'].get_children():
            self.labels['actions'].remove(child)

    def show_restart_buttons(self):

        self.clear_action_bar()
        if self.ks_printer_cfg is not None and self._screen._ws.connected:
            power_devices = self.ks_printer_cfg.get("power_devices", "")
            if power_devices and self._printer.get_power_devices():
                logging.info(f"Associated power devices: {power_devices}")
                self.add_power_button(power_devices)

    def open_info_dialog(self):
        self.dialog = InfoDialog(self.parent, "Değişikler Yapılıyor lütfen bekleyiniz..", False)
        self.dialog.get_style_context().add_class("alert-info-dialog")
      
        self.dialog.set_decorated(False)
        self.dialog.set_size_request(0, 0)
      
     

        response = self.dialog.run()
   
    def finished(self):
        self.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.destroy()


    def add_power_button(self, powerdevs):
        self.labels['power'] = self._gtk.Button("shutdown", _("Power On Printer"), "color3")
        self.labels['power'].connect("clicked", self._screen.power_devices, powerdevs, True)
        self.check_power_status()
        self.labels['actions'].add(self.labels['power'])

    def activate(self):
        self.check_power_status()
        self._screen.base_panel.show_macro_shortcut(False)
        self._screen.base_panel.show_heaters(False)
        self._screen.base_panel.show_estop(False)

    def check_power_status(self):
        if 'power' in self.labels:
            devices = self._printer.get_power_devices()
            if devices is not None:
                for device in devices:
                    if self._printer.get_power_device_status(device) == "off":
                        self.labels['power'].set_sensitive(True)
                        break
                    elif self._printer.get_power_device_status(device) == "on":
                        self.labels['power'].set_sensitive(False)

    def firmware_restart(self, widget):
        self._screen._ws.klippy.restart_firmware()

    def restart(self, widget):
        self._screen._ws.klippy.restart()

    def shutdown(self, widget):
        if self._screen._ws.connected:
            self._screen._confirm_send_action(widget,
                                              _("Are you sure you wish to shutdown the system?"),
                                              "machine.shutdown")
        else:
            logging.info("OS Shutdown")
            os.system("systemctl poweroff")

    def restart_system(self, widget):

        if self._screen._ws.connected:
            self._screen._confirm_send_action(widget,
                                              _("Are you sure you wish to reboot the system?"),
                                              "machine.reboot")
        else:
            logging.info("OS Reboot")
            os.system("systemctl reboot")

    def retry(self, widget):
        self.update_text((_("Connecting to %s") % self._screen.connecting_to_printer))
        if self._screen._ws and not self._screen._ws.connecting:
            self._screen._ws.retry()
        else:
            self._screen.reinit_count = 0
            self._screen.init_printer()
        self.show_restart_buttons()
