import logging
import os
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.macros import Macros
from ks_includes.widgets.systemsetting import SystemSetting
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintSystemSettingScreen(*args)


class CoPrintSystemSettingScreen(ScreenPanel):


    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        menu = BottomMenu(self, False)
    

        update_resp = self._screen.apiclient.send_request("machine/update/status")
        self.update_status = update_resp['result']
        self.version_info = self.update_status['version_info']

        self.version_info['mainsail']['version']

        isUpdateReqKlipper = False
        if self.version_info['klipper']['version'] != self.version_info['klipper']['remote_version']:
            isUpdateReqKlipper = True
        
        isUpdateReqMainsail = False
        if self.version_info['mainsail']['version'] != self.version_info['mainsail']['remote_version']:
            isUpdateReqMainsail = True
        macroone = SystemSetting(self, _("Klipper Update") + " " +_("Current")+ " ("  + self.version_info['klipper']['version'] +")", ("Update"), isUpdateReqKlipper, 'klipper')
        #macrotwo = SystemSetting(self, "Co Print Smart (Current v1.435b)", ("Update"), True)
        macrothree = SystemSetting(self,_("Mainsail") + " "+_("Current") + " (" + self.version_info['mainsail']['version'] +")", ("Update"), isUpdateReqMainsail, 'mainsail')
       
        self.macro_flowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        

        self.macro_flowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.macro_flowbox.pack_start(macroone, True, True, 0)
        #macro_flowbox.pack_start(macrotwo, True, True, 10)
        self.macro_flowbox.pack_start(macrothree, True, True, 0)
        
        updateButton = self._gtk.Button("download", _("Full Update"), "system-full-update", 1.4)
        updateButton.connect("clicked", self.update_program, 'full')
        updateButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        updateButtonBox.set_name("main-button-box")
        updateButtonBox.add(updateButton)
        
        self.refreshButton = self._gtk.Button("redo", _("Refresh"), "system-refresh", 1.4)
        self.refreshButton.connect("clicked", self.refresh_updates)
        refreshButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        refreshButtonBox.set_name("main-button-box")
        refreshButtonBox.add(self.refreshButton)
        
        restartButton = self._gtk.Button("reload", _("Restart"), "system-restart", 1.6)
        #restartButton.connect("clicked", self.open_info_dialog)
        restartButton.connect("clicked", self.reboot_poweroff, "reboot")
        restartButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        restartButtonBox.set_name("main-button-box")
        restartButtonBox.add(restartButton)
        
        shutDownButton = self._gtk.Button("power", _("Shut Down"), "system-shut-down", 1.6)
        #shutDownButton.connect("clicked", self.open_info_dialog)
        shutDownButton.connect("clicked", self.reboot_poweroff, "poweroff")
        shutDownButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        shutDownButtonBox.set_name("main-button-box")
        shutDownButtonBox.add(shutDownButton)
       
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        buttonBox.set_halign(Gtk.Align.CENTER)
        buttonBox.pack_start(updateButtonBox, False, False, 0)
        buttonBox.pack_start(refreshButtonBox, False, False, 0)
        buttonBox.pack_start(restartButtonBox, False, False, 0)
        buttonBox.pack_start(shutDownButtonBox, False, False, 0)
        
        self.macro_flowbox_parent = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.macro_flowbox_parent.pack_start(self.macro_flowbox, True, True, 0)

        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main.set_hexpand(True)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(self.macro_flowbox_parent, True, True, 0)
        main.pack_start(buttonBox, True, True, 0)
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.set_vexpand(True)
        page.pack_start(main, False, False, 0)
        page.pack_end(menu, False, True, 0)
        
        self.content.add(page)


    def update_program_info(self):
        for child in self.macro_flowbox_parent.get_children():
            self.macro_flowbox_parent.remove(child)
        

        self.macro_flowbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        

        update_resp = self._screen.apiclient.send_request("machine/update/status")
        self.update_status = update_resp['result']
        self.version_info = self.update_status['version_info']

        self.version_info['mainsail']['version']

        isUpdateReqKlipper = False
        if self.version_info['klipper']['version'] != self.version_info['klipper']['remote_version']:
            isUpdateReqKlipper = True
        
        isUpdateReqMainsail = False
        if self.version_info['mainsail']['version'] != self.version_info['mainsail']['remote_version']:
            isUpdateReqMainsail = True
        macroone = SystemSetting(self, _("Klipper Update") + " " +_("Current")+ " ("  + self.version_info['klipper']['version'] +")", ("Update"), isUpdateReqKlipper, 'klipper')
        #macrotwo = SystemSetting(self, "Co Print Smart (Current v1.435b)", ("Update"), True)
        macrothree = SystemSetting(self,_("Mainsail") + " "+_("Current") + " (" + self.version_info['mainsail']['version'] +")", ("Update"), isUpdateReqMainsail, 'mainsail')


        self.macro_flowbox.pack_start(macroone, True, True, 0)
        self.macro_flowbox.pack_start(macrothree, True, True, 0)

     

        self.macro_flowbox_parent.pack_start(self.macro_flowbox, True, True, 0)
        self.content.show_all()

    def refresh_updates(self, widget=None):
        self.refreshButton.set_sensitive(False)
        self._screen.show_popup_message(_("Checking for updates, please wait..."), level=1)
        GLib.timeout_add_seconds(1, self.get_updates, "true")

    def get_updates(self, refresh="false"):
        update_resp = self._screen.apiclient.send_request(f"machine/update/status?refresh={refresh}")
        if not update_resp:
            self.update_status = {}
            logging.info("No update manager configured")
        else:
            self.update_status = update_resp['result']
            vi = update_resp['result']['version_info']
            items = sorted(list(vi))
            
            self.update_program_info()
        self.refreshButton.set_sensitive(True)
        self._screen.close_popup_message()


    def update_program(self, widget, program):
        if self._screen.updating or not self.update_status:
            return

        if program in self.update_status['version_info']:
            info = self.update_status['version_info'][program]
            logging.info(f"program: {info}")
            if "package_count" in info and info['package_count'] == 0 \
                    or "version" in info and info['version'] == info['remote_version']:
                return
        self._screen.base_panel.show_update_dialog()
        msg = _("Updating") if program == "full" else _("Starting update for") + f' {program}...'
        self._screen._websocket_callback("notify_update_response",
                                         {'application': {program}, 'message': msg, 'complete': False})

        if program in ['klipper', 'moonraker', 'system', 'full']:
            logging.info(f"Sending machine.update.{program}")
            self._screen._ws.send_method(f"machine.update.{program}")
        else:
            logging.info(f"Sending machine.update.client name: {program}")
            self._screen._ws.send_method("machine.update.client", {"name": program})

    def reboot_poweroff(self, widget, method):
        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)
        if method == "reboot":
            label = Gtk.Label(label=_("Are you sure you wish to reboot the system?"))
        else:
            label = Gtk.Label(label=_("Are you sure you wish to shutdown the system?"))
        vbox.add(label)
        scroll.add(vbox)
        buttons = [
            {"name": _("Host"), "response": Gtk.ResponseType.OK},
            {"name": _("Printer"), "response": Gtk.ResponseType.APPLY},
            {"name": _("Cancel"), "response": Gtk.ResponseType.CANCEL}
        ]
        dialog = self._gtk.Dialog(self._screen, buttons, scroll, self.reboot_poweroff_confirm, method)
        if method == "reboot":
            dialog.set_title(_("Restart"))
        else:
            dialog.set_title(_("Shut Down"))

    def reboot_poweroff_confirm(self, dialog, response_id, method):
        self._gtk.remove_dialog(dialog)
        if response_id == Gtk.ResponseType.OK:
            if method == "reboot":
                os.system("systemctl reboot")
            else:
                os.system("systemctl poweroff")
        elif response_id == Gtk.ResponseType.APPLY:
            if method == "reboot":
                self._screen._ws.send_method("machine.reboot")
            else:
                self._screen._ws.send_method("machine.shutdown")

    
    