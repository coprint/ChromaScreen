import logging
import os
import subprocess
import gi
from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from screen import cd
from ks_includes.screen_panel import ScreenPanel

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)        
        image = self._gtk.Image("coPrint", self._gtk.content_width , self._gtk.content_height * .20)
        spinner = Gtk.Spinner()
        spinner.start()
        initHeader = InitHeader (self, "", _('The settings file is being created. During this time Please wait and do not turn off ChromaScreen.'), "")
        self.image = self._gtk.Image("usb-wait", self._gtk.content_width * .4 , self._gtk.content_height * .4)
        self.labels['text'] = Gtk.Label(_("Creating..."), name="loading-label")
        scroll = self._gtk.ScrolledWindow()
        scroll.set_hexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(spinner)
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)        
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(self.labels['text'], False, False, 100)
        main.pack_start(scroll, True, True, 0)
        self.show_restart_buttons()
        self.content.add(main)

    def update_text(self, text):
        self.show_restart_buttons()

    def start_timer(self):
        """ Start the timer. """
        self.timeout_id = GLib.timeout_add(1500, self.on_timeout, None)
        
    def on_timeout(self, *args, **kwargs):
        path = self._screen.klipper_path
        self._screen.kconfig.write_config(path + "/.config")
        with cd(path):
            # we are in ~/Library
            subprocess.call("make")
        GLib.timeout_add_seconds(15,self._screen.show_panel("co_print_sd_card_selection_process_waiting", "co_print_sd_card_selection_process_waiting", None, 2))
        return False

    def show_restart_buttons(self):
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
        self.start_timer()
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
