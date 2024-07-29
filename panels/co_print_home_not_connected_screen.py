import json
import logging
import os
import time
from ks_includes.widgets.addnetworkdialog import AddNetworkDialog
from ks_includes.widgets.areyousuredialog import AreYouSureDialog
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from ks_includes.functions import internet_on
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.infodialog import InfoDialog
from ks_includes.widgets.keypad import Keypad
from ks_includes.widgets.progressbar import ProgressBar
from ks_includes.widgets.mainbutton import MainButton
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf
from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintHomeNotConnectedScreen(*args)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# class CoPrintHomeNotConnectedScreen(ScreenPanel, metaclass=Singleton):
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
        self.firmwareRestartButton = Gtk.Button(name ="system-restart-"+self.statusLight+"-button") #kırmızısı için name şu class ile değişilecek: system-restart-red-button #
        self.firmwareRestartButton.add(firmwareRestartBox)
        self.firmwareRestartButton.connect("clicked", self.on_click_firmware_restart)
        self.firmwareRestartButton.set_always_show_image (True)

        self.restartBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)     
        self.restartBox.pack_start(self.systemRestartButton, False, False, 0)
        self.restartBox.pack_start(self.firmwareRestartButton, False, False, 0)

        #-----log files-----#
        
        logFilesLabel = Gtk.Label(_("Log Files"), name="bottom-menu-label") 
        logFilesLabel.set_justify(Gtk.Justification.LEFT)
        logFilesLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        logFilesLabelBox.set_name("log-files-label-box")
        logFilesLabelBox.pack_start(logFilesLabel, False, False, 0)

        downloadIcon = self._gtk.Image("download-blue", 20, 20)
        klipperLabel = Gtk.Label(_("Klipper"), name="bottom-menu-label")            
        klipperBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        klipperBox.set_halign(Gtk.Align.CENTER)
        klipperBox.set_valign(Gtk.Align.CENTER)
        klipperBox.pack_start(downloadIcon, False, False, 0)
        klipperBox.pack_start(klipperLabel, False, False, 0)
        self.klipperButton = Gtk.Button(name ="log-files-button")
        self.klipperButton.add(klipperBox)
        self.klipperButton.connect("clicked", self.log_files, 'klippy.log')
        self.klipperButton.set_always_show_image (True)

        downloadIcon = self._gtk.Image("download-blue", 20, 20)
        moonrakerLabel = Gtk.Label(_("Moonraker"), name="bottom-menu-label")            
        moonrakerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        moonrakerBox.set_halign(Gtk.Align.CENTER)
        moonrakerBox.set_valign(Gtk.Align.CENTER)
        moonrakerBox.pack_start(downloadIcon, False, False, 0)
        moonrakerBox.pack_start(moonrakerLabel, False, False, 0)
        self.moonrakerButton = Gtk.Button(name ="log-files-button")
        self.moonrakerButton.add(moonrakerBox)
        self.moonrakerButton.connect("clicked", self.log_files, 'moonraker.log')
        self.moonrakerButton.set_always_show_image (True)

        logFilesButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        logFilesButtonBox.set_halign(Gtk.Align.CENTER)
        logFilesButtonBox.pack_start(self.klipperButton, False, False, 0)
        logFilesButtonBox.pack_start(self.moonrakerButton, False, False, 0)

        logFilesBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        logFilesBox.set_name("log-files-box")
        logFilesBox.pack_start(logFilesLabelBox, False, False, 0)
        logFilesBox.pack_start(logFilesButtonBox, False, False, 0)

        restartButtonsAndLogFilesBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        restartButtonsAndLogFilesBox.pack_start(self.restartBox, False, False, 0)
        #restartButtonsAndLogFilesBox.pack_start(logFilesBox, False, False, 0)


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
        self.IsKlipperNeedUpdate = False
        self.IsMainsailNeedUpdate = False
        if(self.config_data != None) and (self.version_info != False) : 
            if( self.clean_version(self.config_data['KlipperVersion']) > self.clean_version(self.version_info['klipper']['remote_version'])):
                self.IsKlipperNeedUpdate = True
            if(self.clean_version(self.config_data['MainsailVersion']) > self.clean_version(self.version_info['mainsail']['remote_version'])):
                self.IsMainsailNeedUpdate = True
        isUpdateReqKlipper = False
        if self.version_info and self.version_info['klipper']['version'] != self.version_info['klipper']['remote_version']:
            isUpdateReqKlipper = True
        isUpdateReqMainsail = False
        if self.version_info and self.version_info['mainsail']['version'] != self.version_info['mainsail']['remote_version']:
            isUpdateReqMainsail = True
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
            #klipperUpdateButton.connect("clicked", self.klipperUpdateButton)
            klipperVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            klipperVersionBox.pack_start(klipperUpdateLabelBox, False, False, 0)
            klipperVersionBox.pack_start(klipperVersionLabelBox, False, False, 0)
        klipperUpdateBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        klipperUpdateBox.set_name("update-box")
        klipperUpdateBox.pack_start(klipperVersionBox, False, False, 0)
        klipperUpdateBox.pack_end(klipperUpdateButton, False, False, 0)
        box_array.append(klipperUpdateBox)
        #-----mainsail update-----#
        mainsailUpdateLabel = Gtk.Label(_("Mainsail"), name="kipper-label")
        mainsailUpdateLabel.set_justify(Gtk.Justification.LEFT)
        mainsailUpdateLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainsailUpdateLabelBox.pack_start(mainsailUpdateLabel, False, False, 0)

        label_text_mainsail = ''
        if self.version_info:
            label_text_mainsail = _(self.version_info['mainsail']['version'])
        mainsailVersionLabel = Gtk.Label(_("Version: ") + label_text_mainsail, name="klipper-version-label")
        mainsailVersionLabel.set_justify(Gtk.Justification.LEFT)
        mainsailVersionLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainsailVersionLabelBox.pack_start(mainsailVersionLabel, False, False, 0)
        if isUpdateReqMainsail:
            mainsailUpdateButton = Gtk.Button(_('Update'),name ="update-manager-button")
            mainsailUpdateButton.connect("clicked", self.VersionControl, "mainsail")
            mainsailVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            mainsailVersionBox.pack_start(mainsailUpdateLabelBox, False, False, 0)
            mainsailVersionBox.pack_start(mainsailVersionLabelBox, False, False, 0)
        else:
            mainsailUpdateButton = Gtk.Button(_('Up-to-date'),name ="up-to-date-button")
            #klipperUpdateButton.connect("clicked", self.klipperUpdateButton)
            mainsailVersionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            mainsailVersionBox.pack_start(mainsailUpdateLabelBox, False, False, 0)
            mainsailVersionBox.pack_start(mainsailVersionLabelBox, False, False, 0)
        mainsailUpdateBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainsailUpdateBox.set_name("update-box")
        mainsailUpdateBox.pack_start(mainsailVersionBox, False, False, 0)
        mainsailUpdateBox.pack_end(mainsailUpdateButton, False, False, 0)
        box_array.append(mainsailUpdateBox)
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
            #klipperUpdateButton.connect("clicked", self.klipperUpdateButton)
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
        #settingButtonBox.add(settingButton)
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
    
    def clean_version(self, version_str):
        # Başlangıçtaki 'v' karakterini kaldır
        if version_str.startswith('v'):
            version_str = version_str[1:]
        # Ana versiyon numarasını ve ek bilgiyi ayrıştır
        if '-' in version_str:
            main_version, build = version_str.split('-')
            build = int(build)
        else:
            main_version = version_str
            build = 0  # Eğer ek bilgi yoksa build 0 olarak kabul edilir
        # Ana versiyon numarasını parçalarına ayır (major, minor, patch)
        major, minor, patch = map(int, main_version.split('.'))
        return major, minor, patch, build
    
    def VersionControl(self, widget, name):
        if name == 'ChromaScreen':
            self._screen.base_panel.open_dialog()
        else:
            isDialogShow = True
            # if name == "klipper" and self.IsKlipperNeedUpdate:
            #     isDialogShow = False
            # if name == "mainsail" and self.IsMainsailNeedUpdate:
            #     isDialogShow = False
            # if name == "moonraker" and self.IsMoonrakerNeedUpdate:
            #     isDialogShow = False
            # if name == "full" and (self.IsMainsailNeedUpdate and self.self.IsKlipperNeedUpdate):
            #     isDialogShow = False
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

    def on_switch_activated(self, switch, gparam,switchName):
        if switch.get_active():
            if(switchName == 'extruder'):
                temp = self.extruder_temp_target_pre
            else:
                temp = self.heater_bed_temp_target_pre
        else:
            temp = 0
            if(switchName == 'extruder'):
                self.extruder_temp_target_pre = temp
            else:
                self.heater_bed_temp_target_pre = temp

        if(switchName == 'extruder'):
            self.change_extruder_temperature(temp)
        else:
            self.change_bed_temperature(temp)

    def chanceExtruder(self, eventBox, gparam, extruder):
        index = next((i for i, item in enumerate(self.extruders) if item['Extrude'] == extruder), -1)
        oldIndex = next((i for i, item in enumerate(self.extruders) if item['Extrude'] == self._printer.data["toolhead"]["extruder"]), -1)
        self.extruders[oldIndex]['EventBox'].get_style_context().remove_class("extrude-active")
        self.extruders[index]['EventBox'].get_style_context().add_class("extrude-active")
        self.connectedExtruder.set_label(extruder)
        self._screen._ws.klippy.gcode_script("T" + str(index))

    def on_color_set(self, colorbutton):
        color = colorbutton.get_rgba()
        red = int(color.red * 255)
        green = int(color.green * 255)
        blue = int(color.blue * 255)

    def select_heater(self, widget, device):
        if self.active_heater is None and device in self.devices and self.devices[device]["can_target"]:
            if device in self.active_heaters:
                self.active_heaters.pop(self.active_heaters.index(device))
                self.devices[device]['name'].get_style_context().remove_class("button_active")
                self.devices[device]['select'].set_label(_("Select"))
                logging.info(f"Deselecting {device}")
                return
            self.active_heaters.append(device)
            self.devices[device]['name'].get_style_context().add_class("button_active")
            self.devices[device]['select'].set_label(_("Deselect"))
            logging.info(f"Seselecting {device}")
        return

    def change_bed_temperature(self, temp):
        max_temp = float(self._printer.get_config_section('heater_bed')['max_temp'])
        if self.validate('heater_bed', temp, max_temp):
            self._screen._ws.klippy.set_bed_temp(temp)

    def change_extruder_temperature(self,temp):
        max_temp = float(self._printer.get_config_section(self._printer.data["toolhead"]["extruder"])['max_temp'])
        if self.validate(self._printer.data["toolhead"]["extruder"], temp, max_temp):
            self._screen._ws.klippy.set_tool_temp(self._printer.get_tool_number(self._printer.data["toolhead"]["extruder"]), temp)

    def change_bed_temperature_pre(self, target):
        max_temp = float(self._printer.get_config_section('heater_bed')['max_temp'])
        if self.validate('heater_bed', target, max_temp):
            self.heater_bed_temp_target_pre = target
        if self.heater_bed_temp_target_pre > 0 :
            self.heatedBedSwitch.set_active(True)
        else :
             self.heatedBedSwitch.set_active(False)
        self.change_bed_temperature(self.heater_bed_temp_target_pre)

    def change_extruder_temperature_pre(self, target):
        max_temp = float(self._printer.get_config_section(self._printer.data["toolhead"]["extruder"])['max_temp'])
        if self.validate(self._printer.data["toolhead"]["extruder"], target, max_temp):
            self.extruder_temp_target_pre = target
        if self.extruder_temp_target_pre > 0 :
            self.extruderSwitch.set_active(True)
        else :
             self.extruderSwitch.set_active(False)
        self.change_extruder_temperature(self.extruder_temp_target_pre)


    def set_temperature(self, widget, setting):
        if len(self.active_heaters) == 0:
            self._screen.show_popup_message(_("Nothing selected"))
        else:
            for heater in self.active_heaters:
                target = None
                max_temp = float(self._printer.get_config_section(heater)['max_temp'])
                name = heater.split()[1] if len(heater.split()) > 1 else heater
                with contextlib.suppress(KeyError):
                    for i in self.preheat_options[setting]:
                        logging.info(f"{self.preheat_options[setting]}")
                        if i == name:
                            # Assign the specific target if available
                            target = self.preheat_options[setting][name]
                            logging.info(f"name match {name}")
                        elif i == heater:
                            target = self.preheat_options[setting][heater]
                            logging.info(f"heater match {heater}")
                if target is None and setting == "cooldown" and not heater.startswith('temperature_fan '):
                    target = 0
                else:

                    self.heatedBedSwitch.set_active(True)
                    self.extruderSwitch.set_active(True)
                if heater.startswith('extruder'):
                    if self.validate(heater, target, max_temp):
                        self._screen._ws.klippy.set_tool_temp(self._printer.get_tool_number(heater), target)
                        self.extruder_temp_target_pre = target
                elif heater.startswith('heater_bed'):
                    if target is None:
                        with contextlib.suppress(KeyError):
                            target = self.preheat_options[setting]["bed"]
                    if self.validate(heater, target, max_temp):
                        self._screen._ws.klippy.set_bed_temp(target)
                        self.heater_bed_temp_target_pre = target
                elif heater.startswith('heater_generic '):
                    if target is None:
                        with contextlib.suppress(KeyError):
                            target = self.preheat_options[setting]["heater_generic"]
                    if self.validate(heater, target, max_temp):
                        self._screen._ws.klippy.set_heater_temp(name, target)
                elif heater.startswith('temperature_fan '):
                    if target is None:
                        with contextlib.suppress(KeyError):
                            target = self.preheat_options[setting]["temperature_fan"]
                    if self.validate(heater, target, max_temp):
                        self._screen._ws.klippy.set_temp_fan_temp(name, target)
            # This small delay is needed to properly update the target if the user configured something above
            # and then changed the target again using preheat gcode
            GLib.timeout_add(250, self.preheat_gcode, setting)


    def preheat_gcode(self, setting):
        with contextlib.suppress(KeyError):
            self._screen._ws.klippy.gcode_script(self.preheat_options[setting]['gcode'])
        return False
    def validate(self, heater, target=None, max_temp=None):
        if target is not None and max_temp is not None:
            if 0 <= target <= max_temp:
                self._printer.set_dev_stat(heater, "target", target)
                return True
            elif target > max_temp:
                self._screen.show_popup_message(_("Can't set above the maximum:") + f' {max_temp}')
                return False
        logging.debug(f"Invalid {heater} Target:{target}/{max_temp}")
        return False

    def add_device(self, device):


        logging.info(f"Adding device: {device}")

        temperature = self._printer.get_dev_stat(device, "temperature")
        if temperature is None:
            return False

        devname = device.split()[1] if len(device.split()) > 1 else device
        # Support for hiding devices by name
        if devname.startswith("_"):
            return False

        if device.startswith("extruder"):
            i = sum(d.startswith('extruder') for d in self.devices)
            image = f"extruder-{i}" if self._printer.extrudercount > 1 else "extruder"
            class_name = f"graph_label_{device}"
            dev_type = "extruder"
        elif device == "heater_bed":
            image = "bed"
            devname = "Heater Bed"
            class_name = "graph_label_heater_bed"
            dev_type = "bed"
        elif device.startswith("heater_generic"):
            self.h = sum("heater_generic" in d for d in self.devices)
            image = "heater"
            class_name = f"graph_label_sensor_{self.h}"
            dev_type = "sensor"
        elif device.startswith("temperature_fan"):
            f = 1 + sum("temperature_fan" in d for d in self.devices)
            image = "fan"
            class_name = f"graph_label_fan_{f}"
            dev_type = "fan"
        elif self._config.get_main_config().getboolean("only_heaters", False):
            return False
        else:
            self.h += sum("sensor" in d for d in self.devices)
            image = "heat-up"
            class_name = f"graph_label_sensor_{self.h}"
            dev_type = "sensor"

        rgb = self._gtk.get_temp_color(dev_type)

        name = self._gtk.Button(image, devname.capitalize().replace("_", " "), None, self.bts, Gtk.PositionType.LEFT, 1)
        name.set_alignment(0, .5)
        visible = self._config.get_config().getboolean(f"graph {self._screen.connected_printer}", device, fallback=True)
        if visible:
            name.get_style_context().add_class(class_name)
        else:
            name.get_style_context().add_class("graph_label_hidden")

        can_target = self._printer.device_has_target(device)

        if can_target:

            name.connect('button-press-event', self.name_pressed, device)
            name.connect('button-release-event', self.name_released, device)
        else:
            name.connect("clicked", self.toggle_visibility, device)


        temp = self._gtk.Button(label="", lines=1)
        if can_target:
            temp.connect("clicked", self.show_numpad, device)

        self.devices[device] = {
            "class": class_name,
            "name": name,
            "temp": temp,
            "can_target": can_target,
            "visible": visible
        }

        if self.devices[device]["can_target"]:
            self.devices[device]['select'] = self._gtk.Button(label=_("Select"))
            self.devices[device]['select'].connect('clicked', self.select_heater, device)



        return True


    def name_pressed(self, widget, event, device):
        self.popover_timeout = GLib.timeout_add_seconds(1, self.popover_popup, widget, device)

    def name_released(self, widget, event, device):
        if self.popover_timeout is not None:
            GLib.source_remove(self.popover_timeout)
            self.popover_timeout = None
        if not self.popover_device:
            self.select_heater(None, device)

    def toggle_visibility(self, widget, device=None):
        if device is None:
            device = self.popover_device
        self.devices[device]['visible'] ^= True
        logging.info(f"Graph show {self.devices[device]['visible']}: {device}")

        section = f"graph {self._screen.connected_printer}"
        if section not in self._config.get_config().sections():
            self._config.get_config().add_section(section)
        self._config.set(section, f"{device}", f"{self.devices[device]['visible']}")
        self._config.save_user_config_options()

        self.update_graph_visibility()
        if self.devices[device]['can_target']:
            self.popover_populate_menu()
            self.labels['popover'].show_all()

    def show_numpad(self, widget, device=None):
        for d in self.active_heaters:
            self.devices[d]['name'].get_style_context().remove_class("button_active")
        self.active_heater = self.popover_device if device is None else device
        self.devices[self.active_heater]['name'].get_style_context().add_class("button_active")

        if "keypad" not in self.labels:
            self.labels["keypad"] = Keypad(self._screen, self.change_target_temp, self.hide_numpad)
        self.labels["keypad"].clear()

        if self._screen.vertical_mode:
            self.grid.remove_row(1)
            self.grid.attach(self.labels["keypad"], 0, 1, 1, 1)
        else:
            self.grid.remove_column(1)
            self.grid.attach(self.labels["keypad"], 1, 0, 1, 1)
        self.grid.show_all()

        self.labels['popover'].popdown()

    def __del__(self):
        self.desiredTemp = 1
        print('Destructor called, Employee deleted.')

    def del_obj(self):
        self.desiredTemp = 1
        self.extruderChanged = False

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
