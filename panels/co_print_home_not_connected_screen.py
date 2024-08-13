import json
import logging
import os
import time
from ks_includes.widgets.areyousuredialog import AreYouSureDialog
import gi
import contextlib
from ks_includes.functions import internet_on
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.keypad import Keypad
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from ks_includes.screen_panel import ScreenPanel
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
class Panel(ScreenPanel, metaclass=Singleton):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        box_array = []
        self.current_time_millis = int(round(time.time() * 1000))
        menu = BottomMenu(self, False)
        self.state = self._printer.state
        self.state_message = self._printer.state_message
        #-----LEFT BOX-----#
        #-----warning report-----#
        self.statusLight = 'yellow'
        if self._printer.state == 'error':
            self.statusLight = 'red'
        elif self._printer.state == 'startup':
            self.statusLight = 'blue'
        reportHeaderBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        warningYellowIcon = self._gtk.Image("warning-"+self.statusLight, 35, 35)
        warningHeaderLabel = Gtk.Label(_("Klipper reports: "+ (self._printer.state).upper()), name="warning-header-"+self.statusLight+"-label") #kırmızısı için name şu class ile değişilecek: warning-header-red-label #
        reportHeaderBox.pack_start(warningYellowIcon, False, False, 0)
        reportHeaderBox.pack_start(warningHeaderLabel, False, False, 0)
        warningContentLabel = Gtk.Label((self._printer.state_message).replace('\n', ' '), name="warning-content-"+self.statusLight+"-label") #kırmızısı için name şu class ile değişilecek: warning-content-red-label #
        warningContentLabel.set_max_width_chars(65)
        warningContentLabel.set_line_wrap(True)
        warningContentLabel.set_justify(Gtk.Justification.LEFT)
        waringContentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        waringContentBox.pack_start(warningContentLabel, False, False, 0)
        self.reportBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.reportBox.set_name("report-box-" + self.statusLight)
        self.reportBox.pack_start(reportHeaderBox, False, False, 0)
        self.reportBox.pack_start(waringContentBox, False, False, 0)
        #-----system restart button-----#
        systemRestartIcon = self._gtk.Image("redo", 35, 35)
        systemRestartLabel = Gtk.Label(_("System Restart"), name="bottom-menu-label")            
        systemRestartBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        systemRestartBox.set_halign(Gtk.Align.CENTER)
        systemRestartBox.set_valign(Gtk.Align.CENTER)
        systemRestartBox.pack_start(systemRestartIcon, False, False, 0)
        systemRestartBox.pack_start(systemRestartLabel, False, False, 0)
        self.systemRestartButton = Gtk.Button(name ="system-restart-"+self.statusLight+"-button")
        self.systemRestartButton.add(systemRestartBox)
        self.systemRestartButton.connect("clicked", self.reboot_poweroff, 'reboot')
        self.systemRestartButton.set_always_show_image (True)
        #-----firmware restart button-----#
        firmwareRestartIcon = self._gtk.Image("reload", 35, 35)
        firmwareRestartLabel = Gtk.Label(_("Firmware Restart"), name="bottom-menu-label")            
        firmwareRestartBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        firmwareRestartBox.set_halign(Gtk.Align.CENTER)
        firmwareRestartBox.set_valign(Gtk.Align.CENTER)
        firmwareRestartBox.pack_start(firmwareRestartIcon, False, False, 0)
        firmwareRestartBox.pack_start(firmwareRestartLabel, False, False, 0)
        self.firmwareRestartButton = Gtk.Button(name ="system-restart-"+self.statusLight+"-button")
        self.firmwareRestartButton.add(firmwareRestartBox)
        self.firmwareRestartButton.connect("clicked", self.on_click_firmware_restart)
        self.firmwareRestartButton.set_always_show_image (True)
        self.restartBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)     
        self.restartBox.pack_start(self.systemRestartButton, False, False, 0)
        self.restartBox.pack_start(self.firmwareRestartButton, False, False, 0)
        
        restartButtonsAndLogFilesBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        restartButtonsAndLogFilesBox.pack_start(self.restartBox, False, False, 0)
        #-----update maganer-----#
        updateIcon = self._gtk.Image("upload", 25, 25)
        updateManagerLabel = Gtk.Label(_("Update Manager"))
        updateManagerLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        updateManagerLabelBox.set_name("update-manager-label-box")
        updateManagerLabelBox.pack_start(updateIcon, False, False, 0)
        updateManagerLabelBox.pack_start(updateManagerLabel, False, False, 0)
        
        update_resp = self._screen.apiclient.send_request("machine/update/status")
        if update_resp:
            self.update_status = update_resp['result']
            self.version_info = self.update_status['version_info']
        else:
            self.update_status = False
            self.version_info = False
        self.config_data = None
        try:
            f = open(self._screen.path_config, encoding='utf-8')
            self.config_data = json.load(f)
        except Exception as e:
            logging.exception(e) 
        self.ChromaScreenNeedUpdate = self._screen.base_panel.need_update()
        isUpdateReqKlipper = False
        if self.version_info and self.version_info['klipper']['version'] != self.version_info['klipper']['remote_version']:
            isUpdateReqKlipper = True
        # isUpdateReqMainsail = False
        # if self.version_info and self.version_info['mainsail']['version'] != self.version_info['mainsail']['remote_version']:
        #     isUpdateReqMainsail = True
        isUpdateReqMoonraker = False
        if self.version_info and self.version_info['moonraker']['version'] != self.version_info['moonraker']['remote_version']:
            isUpdateReqMoonraker = True
        #-----chromascreen update-----#
        chromascreenUpdateLabel = Gtk.Label(_("Chromascreen"), name="kipper-label")
        chromascreenUpdateLabel.set_justify(Gtk.Justification.LEFT)
        chromascreenUpdateLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        chromascreenUpdateLabelBox.pack_start(chromascreenUpdateLabel, False, False, 0)
        chromascreenVersionLabel = Gtk.Label(_("Version: ") + self._screen.version, name="klipper-version-label")
        chromascreenVersionLabel.set_justify(Gtk.Justification.LEFT)
        chromascreenVersionLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        chromascreenVersionLabelBox.pack_start(chromascreenVersionLabel, False, False, 0)
        if self.ChromaScreenNeedUpdate:
            chromascreenUpdateButton = Gtk.Button(_('Update'),name ="update-manager-button")
            chromascreenUpdateButton.connect("clicked", self.VersionControl, "ChromaScreen")
            chromascreenVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            chromascreenVersionBox.pack_start(chromascreenUpdateLabelBox, False, False, 0)
            chromascreenVersionBox.pack_start(chromascreenVersionLabelBox, False, False, 0)
        else:
            chromascreenUpdateButton = Gtk.Button(_('Up-to-date'),name ="up-to-date-button")
            chromascreenVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            chromascreenVersionBox.pack_start(chromascreenUpdateLabelBox, False, False, 0)
            chromascreenVersionBox.pack_start(chromascreenVersionLabelBox, False, False, 0)
        chromascreenUpdateBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        chromascreenUpdateBox.set_name("update-box")
        chromascreenUpdateBox.pack_start(chromascreenVersionBox, False, False, 0)
        chromascreenUpdateBox.pack_end(chromascreenUpdateButton, False, False, 0)
        box_array.append(chromascreenUpdateBox)
        #-----klipper update-----#
        klipperUpdateLabel = Gtk.Label(_("Klipper"), name="kipper-label")
        klipperUpdateLabel.set_justify(Gtk.Justification.LEFT)
        klipperUpdateLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        klipperUpdateLabelBox.pack_start(klipperUpdateLabel, False, False, 0)
        label_text = ''
        if self.version_info:
            label_text = _(self.version_info['klipper']['version'])
        klipperVersionLabel = Gtk.Label(_("Version: ") + label_text, name="klipper-version-label")
        klipperVersionLabel.set_justify(Gtk.Justification.LEFT)
        klipperVersionLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        klipperVersionLabelBox.pack_start(klipperVersionLabel, False, False, 0)
        if isUpdateReqKlipper:
            klipperUpdateButton = Gtk.Button(_('Update'),name ="update-manager-button")
            klipperUpdateButton.connect("clicked", self.VersionControl, "klipper")
            klipperVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            klipperVersionBox.pack_start(klipperUpdateLabelBox, False, False, 0)
            klipperVersionBox.pack_start(klipperVersionLabelBox, False, False, 0)
        else:
            klipperUpdateButton = Gtk.Button(_('Up-to-date'),name ="up-to-date-button")
            klipperVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            klipperVersionBox.pack_start(klipperUpdateLabelBox, False, False, 0)
            klipperVersionBox.pack_start(klipperVersionLabelBox, False, False, 0)
        klipperUpdateBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        klipperUpdateBox.set_name("update-box")
        klipperUpdateBox.pack_start(klipperVersionBox, False, False, 0)
        klipperUpdateBox.pack_end(klipperUpdateButton, False, False, 0)
        box_array.append(klipperUpdateBox)
        #-----mainsail update-----#
        # mainsailUpdateLabel = Gtk.Label(_("Mainsail"), name="kipper-label")
        # mainsailUpdateLabel.set_justify(Gtk.Justification.LEFT)
        # mainsailUpdateLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # mainsailUpdateLabelBox.pack_start(mainsailUpdateLabel, False, False, 0)
        # label_text_mainsail = ''
        # if self.version_info:
        #     label_text_mainsail = _(self.version_info['mainsail']['version'])
        # mainsailVersionLabel = Gtk.Label(_("Version: ") + label_text_mainsail, name="klipper-version-label")
        # mainsailVersionLabel.set_justify(Gtk.Justification.LEFT)
        # mainsailVersionLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # mainsailVersionLabelBox.pack_start(mainsailVersionLabel, False, False, 0)
        # if isUpdateReqMainsail:
        #     mainsailUpdateButton = Gtk.Button(_('Update'),name ="update-manager-button")
        #     mainsailUpdateButton.connect("clicked", self.VersionControl, "mainsail")
        #     mainsailVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        #     mainsailVersionBox.pack_start(mainsailUpdateLabelBox, False, False, 0)
        #     mainsailVersionBox.pack_start(mainsailVersionLabelBox, False, False, 0)
        # else:
        #     mainsailUpdateButton = Gtk.Button(_('Up-to-date'),name ="up-to-date-button")
        #     mainsailVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        #     mainsailVersionBox.pack_start(mainsailUpdateLabelBox, False, False, 0)
        #     mainsailVersionBox.pack_start(mainsailVersionLabelBox, False, False, 0)
        # mainsailUpdateBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        # mainsailUpdateBox.set_name("update-box")
        # mainsailUpdateBox.pack_start(mainsailVersionBox, False, False, 0)
        # mainsailUpdateBox.pack_end(mainsailUpdateButton, False, False, 0)
        # box_array.append(mainsailUpdateBox)
        #-----moonraker update-----#
        moonrakerUpdateLabel = Gtk.Label(_("Moonraker"), name="kipper-label")
        moonrakerUpdateLabel.set_justify(Gtk.Justification.LEFT)
        moonrakerUpdateLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        moonrakerUpdateLabelBox.pack_start(moonrakerUpdateLabel, False, False, 0)
        label_text = ''
        if self.version_info:
            label_text = _(self.version_info['moonraker']['version'])
        moonrakerVersionLabel = Gtk.Label(_("Version: ") + label_text, name="klipper-version-label")
        moonrakerVersionLabel.set_justify(Gtk.Justification.LEFT)
        moonrakerVersionLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        moonrakerVersionLabelBox.pack_start(moonrakerVersionLabel, False, False, 0)
        if isUpdateReqMoonraker:
            moonrakerUpdateButton = Gtk.Button(_('Update'),name ="update-manager-button")
            moonrakerUpdateButton.connect("clicked", self.VersionControl, "klipper")
            moonrakerVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            moonrakerVersionBox.pack_start(moonrakerUpdateLabelBox, False, False, 0)
            moonrakerVersionBox.pack_start(moonrakerVersionLabelBox, False, False, 0)
        else:
            moonrakerUpdateButton = Gtk.Button(_('Up-to-date'),name ="up-to-date-button")
            moonrakerVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            moonrakerVersionBox.pack_start(moonrakerUpdateLabelBox, False, False, 0)
            moonrakerVersionBox.pack_start(moonrakerVersionLabelBox, False, False, 0)
        moonrakerUpdateBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        moonrakerUpdateBox.set_name("update-box")
        moonrakerUpdateBox.pack_start(moonrakerVersionBox, False, False, 0)
        moonrakerUpdateBox.pack_end(moonrakerUpdateButton, False, False, 0)
        box_array.append(moonrakerUpdateBox)
        updateManagerBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        updateManagerBox.set_name("update-manager-box")
        updateManagerBox.pack_start(updateManagerLabelBox, False, False, 0)
        for box in box_array:
            updateManagerBox.pack_start(box, False, False, 0)
            separator = Gtk.HSeparator()
            separator.get_style_context().add_class("exp-separator")
            updateManagerBox.pack_start(separator, False, False, 0)
        leftContentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        leftContentBox.set_valign(Gtk.Align.START)
        leftContentBox.pack_start(restartButtonsAndLogFilesBox, False, False, 0)
        leftContentBox.pack_start(updateManagerBox, False, False, 0)
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        left_box.set_halign(Gtk.Align.START)
        left_box.pack_start(self.reportBox, False, False, 0)
        left_box.pack_start(leftContentBox, False, False, 0)
        #-----RIGHT BOX-----#
        coprintQr = self._gtk.Image("coprint-qr", 120, 120)
        wikiHeaderLabel = Gtk.Label(_("Co Print Wiki"), name="wiki-header-green-label")
        wikiContentLabel = Gtk.Label(_("Having trouble installing or starting up? Scan the QR code to get help and detailed information."), name="wiki-content-green-label")
        wikiContentLabel.set_max_width_chars(30)
        wikiContentLabel.set_line_wrap(True)
        wikiContentLabel.set_justify(Gtk.Justification.CENTER)
        wikiContentLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        wikiContentLabelBox.pack_start(wikiContentLabel, False, False, 0)

        wikiBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        wikiBox.set_halign(Gtk.Align.CENTER)
        wikiBox.set_name("wiki-box")
        wikiBox.pack_start(coprintQr, False, False, 0)  
        wikiBox.pack_start(wikiHeaderLabel, False, False, 0)
        wikiBox.pack_start(wikiContentLabelBox, False, False, 0)

        shutDownButton = self._gtk.Button("power", _("Shut Down"), "not-connected-shut-down", 1)
        shutDownButton.connect("clicked", self.reboot_poweroff, "poweroff")
        shutDownButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        shutDownButtonBox.set_name("main-button-box")
        shutDownButtonBox.pack_start(shutDownButton, False, False, 0)
       
        settingButton = self._gtk.Button("network", _("Network"), "not-connected-setting", 1)
        settingButton.connect("clicked", self.network_page, "reboot")
        settingButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        settingButtonBox.set_name("main-button-box")
        settingButtonBox.pack_start(settingButton, False, False, 0)

        menuGrid = Gtk.Grid()
        menuGrid.set_column_spacing(10)
        menuGrid.set_row_spacing(10)
        menuGrid.set_column_homogeneous(True)
        menuGrid.attach(settingButtonBox, 0, 0, 1, 1)
        menuGrid.attach(shutDownButtonBox, 1, 0, 1, 1)
        rightButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        rightButtonBox.pack_start(menuGrid, False, False, 0)

        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        right_box.pack_start(wikiBox, False, True, 0)
        right_box.pack_start(rightButtonBox, False, False, 0)

        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        main_box.pack_start(left_box, True, True, 0)
        main_box.pack_start(right_box, True, True, 0)
        main_box.set_vexpand(True)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.set_valign(Gtk.Align.CENTER)

        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(main_box, True, True, 0)
        page.pack_end(menu, False, True, 0)
        self.content.add(page)

    def generateRestartButtons(self):
        if self.restartBox.get_children() != None:
            for child in self.restartBox.get_children():
                self.restartBox.remove(child)
        #-----system restart button-----#
        systemRestartIcon = self._gtk.Image("redo", 35, 35)
        systemRestartLabel = Gtk.Label(_("System Restart"), name="bottom-menu-label")            
        systemRestartBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        systemRestartBox.set_halign(Gtk.Align.CENTER)
        systemRestartBox.set_valign(Gtk.Align.CENTER)
        systemRestartBox.pack_start(systemRestartIcon, False, False, 0)
        systemRestartBox.pack_start(systemRestartLabel, False, False, 0)
        self.systemRestartButton = Gtk.Button(name ="system-restart-"+self.statusLight+"-button")
        self.systemRestartButton.add(systemRestartBox)
        self.systemRestartButton.connect("clicked", self.reboot_poweroff, 'reboot')
        self.systemRestartButton.set_always_show_image (True)

        #-----firmware restart button-----#
        firmwareRestartIcon = self._gtk.Image("reload", 35, 35)
        firmwareRestartLabel = Gtk.Label(_("Firmware Restart"), name="bottom-menu-label")            
        firmwareRestartBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        firmwareRestartBox.set_halign(Gtk.Align.CENTER)
        firmwareRestartBox.set_valign(Gtk.Align.CENTER)
        firmwareRestartBox.pack_start(firmwareRestartIcon, False, False, 0)
        firmwareRestartBox.pack_start(firmwareRestartLabel, False, False, 0)
        self.firmwareRestartButton = Gtk.Button(name ="system-restart-"+self.statusLight+"-button")
        self.firmwareRestartButton.add(firmwareRestartBox)
        self.firmwareRestartButton.connect("clicked", self.on_click_firmware_restart)
        self.firmwareRestartButton.set_always_show_image (True)
        
        self.restartBox.pack_start(self.systemRestartButton, False, False, 0)
        self.restartBox.pack_start(self.firmwareRestartButton, False, False, 0)
        self.restartBox.show_all()

    def VersionControl(self, widget, name):
        if name == 'ChromaScreen':
            self._screen.base_panel.open_dialog()
        else:
            isDialogShow = True
            if isDialogShow:  
                content = _("Your update may not be compatible with ChromaScreen.\nChromaScreen is compatible with:\nKlipper: v0.12.0-268.\nMoonraker: v0.9.1-0.\nMainsail: v2.12.0.\nStill Do you want to update?")
                dialog = AreYouSureDialog( content, self)
                dialog.get_style_context().add_class("network-dialog")
                dialog.set_decorated(False)
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    self.update_program(None, name)
                    print('Ok')
                    dialog.destroy()
                elif response == Gtk.ResponseType.CANCEL:
                    print('Cancel')
                    dialog.destroy()
            else:
                self.update_program(None, name)

    def log_files(self, widget, type):
        page_url = 'co_print_log_files_screen'
        self._screen.show_panel(page_url, page_url, type, 1, False)

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
    
    def on_click_system_restart(self, button):    
        self._screen._ws.klippy.restart()

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
            {"name": _("Ok"), "response": Gtk.ResponseType.OK},
            {"name": _("Cancel"), "response": Gtk.ResponseType.CANCEL}
        ]
        dialog = self._gtk.Dialog(self._screen, buttons, scroll, self.reboot_poweroff_confirm, method)
        if method == "reboot":
            dialog.set_title(_("Restart"))
        else:
            dialog.set_title(_("Shut Down"))

    def network_page(self, widget, method):
        self._screen.show_panel("co_print_network_setting_screen", "co_print_network_setting_screen", "Language", 1, False)
                    
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
                
    def on_click_firmware_restart(self, button):
        self._screen._ws.klippy.restart_firmware()

    def update_message(self):
        if self.reportBox.get_children() != None:
            for child in self.reportBox.get_children():
                self.reportBox.remove(child)
        self.statusLight = 'yellow'
        if self._printer.state == 'error':
            self.statusLight = 'red'
        elif self._printer.state == 'startup':
            self.statusLight = 'blue'
        reportHeaderBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        warningHeaderLabel = Gtk.Label(_("Klipper reports: "+ (self._printer.state).upper()), name="warning-header-"+self.statusLight+"-label") #kırmızısı için name şu class ile değişilecek: warning-header-red-label #
        if self.statusLight == 'yellow':
            warningYellowIcon = self._gtk.Image("warning-"+self.statusLight, 35, 35)
            reportHeaderBox.pack_start(warningYellowIcon, False, False, 0)
        reportHeaderBox.pack_start(warningHeaderLabel, False, False, 0)
        warningContentLabel = Gtk.Label((self._printer.state_message).replace('\n', ' '), name="warning-content-"+self.statusLight+"-label") #kırmızısı için name şu class ile değişilecek: warning-content-red-label #
        warningContentLabel.set_max_width_chars(65)
        warningContentLabel.set_line_wrap(True)
        warningContentLabel.set_justify(Gtk.Justification.LEFT)
        waringContentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        waringContentBox.pack_start(warningContentLabel, False, False, 0)
        self.reportBox.set_name("report-box-" + self.statusLight)
        self.reportBox.pack_start(reportHeaderBox, False, False, 0)
        self.reportBox.pack_start(waringContentBox, False, False, 0)
        self.reportBox.show_all()
        

    def process_update(self, action, data):

        if self._printer.state != self.state or self.state_message != self._printer.state_message:
            self.state = self._printer.state
            self.state_message = self._printer.state_message
            self.update_message()
            self.generateRestartButtons()
            
        if self._printer.state == 'ready' :
            page_url = 'co_print_home_screen'
            self._screen.show_panel(page_url, page_url, "Language", 1, False) 
