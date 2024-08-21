import json
import logging
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintSplashScreenPanel(*args)


# class CoPrintSplashScreenPanel(ScreenPanel):
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        image = self._gtk.Image("coPrint", self._gtk.content_width , self._gtk.content_height * .20)
        spinner = Gtk.Spinner()
        spinner.start()
        self.labels['text'] = Gtk.Label(_("Initializing printer..."))
        self.labels['text'].set_line_wrap(True)
        self.labels['text'].set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.labels['text'].set_halign(Gtk.Align.CENTER)
        self.labels['text'].set_valign(Gtk.Align.CENTER)

        self.labels['menu'] = self._gtk.Button("settings", _("Menu Noya"), "color4")
        self.labels['menu'].connect("clicked", self._screen._go_to_submenu, "")
        self.labels['restart'] = self._gtk.Button("refresh", _("Klipper Restart"), "color1")
        self.labels['restart'].connect("clicked", self.restart)
        self.labels['firmware_restart'] = self._gtk.Button("refresh", _("Firmware Restart"), "color2")
        self.labels['firmware_restart'].connect("clicked", self.firmware_restart)
        self.labels['restart_system'] = self._gtk.Button("refresh", _("System Restart"), "color1")
        self.labels['restart_system'].connect("clicked", self.restart_system)
        self.labels['shutdown'] = self._gtk.Button("shutdown", _('System Shutdown'), "color2")
        self.labels['shutdown'].connect("clicked", self.shutdown)
        self.labels['retry'] = self._gtk.Button("load", _('Retry'), "color3")
        self.labels['retry'].connect("clicked", self.retry)

        self.labels['actions'] = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.labels['actions'].set_hexpand(True)
        self.labels['actions'].set_vexpand(False)
        self.labels['actions'].set_halign(Gtk.Align.CENTER)
        self.labels['actions'].set_homogeneous(True)
        self.labels['actions'].set_size_request(self._gtk.content_width, -1)

        scroll = self._gtk.ScrolledWindow()
        scroll.set_hexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(spinner)

        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        info.pack_start(image, False, True, 100)
        info.pack_end(scroll, False, False, 20)

        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.pack_start(info, True, True, 0)
        main.pack_end(self.labels['actions'], False, False, 0)
        self.config_data = None
        self.show_restart_buttons()
        try:
            f = open(self._screen.path_config, encoding='utf-8')
       
            self.config_data = json.load(f)
        except Exception as e:
            logging.exception(e) 
       

        self.start_timerr()
        self.content.add(main)
        
        

    def update_text(self):
        
        self.show_restart_buttons()

    def start_timerr(self):
        """ Start the timer. """
        self.timeout_id = GLib.timeout_add(2500, self.on_timeout, None)
        

    def on_timeout(self, *args, **kwargs):
        self.changed = False
        if(self.config_data != None):
            if(self.config_data['InitConfigDone'] == False):
                self.changed = True
                self._screen.show_panel("co_print_language_select_screen", "co_print_language_select_screen", "Language", 1, False)
            elif(self.config_data['Printer1WizardDone'] == False):
                self.changed = True
                self._screen.show_panel("co_print_printing_brand_selection_new", "co_print_printing_brand_selection_new", "Language", 1, False)
           


        if(self.changed == False):
            if self._screen.connected_printer :
                if self._printer.state == 'error' or self._printer.state == 'shutdown' or self._printer.state ==  'disconnected':

                    self._screen.show_panel("co_print_home_not_connected_screen", "co_print_home_not_connected_screen", "Language", 1, False)
                    #self._screen.show_panel("co_print_home_not_connected_screen", "co_print_home_not_connected_screen", "Language", 1, False)
                else:
                    self._screen.show_panel("co_print_home_screen", "co_print_home_screen", "Language", 1, False)
                    #self._screen.show_panel("co_print_home_screen", "co_print_home_screen", "Language", 1, False)
            else:
                self._screen.show_panel("co_print_home_not_connected_screen", "co_print_home_not_connected_screen", "Language", 1, False)

        
       
        
        self.timeout_id = None
        #self.destroy()
        return False
    
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
        self.update_text()
        if self._screen._ws and not self._screen._ws.connecting:
            self._screen._ws.retry()
        else:
            self._screen.reinit_count = 0
            self._screen.init_printer()
        self.show_restart_buttons()
