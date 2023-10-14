import logging
import os
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.mainbutton import MainButton
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintSettingScreen(*args)


class CoPrintSettingScreen(ScreenPanel):

    active_heater = None
    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        
        
        probeCalibrationButton = MainButton(self, "zprobe", _("Probe Calibration"), "probe-calibration", "co_print_probe_calibration_screen",2, False)
        autoLevelingButton = MainButton(self, "autoleveling", _("Auto Leveling"), "auto-leveling", 'co_print_auto_leveling_screen',2, False)
        manuelLevelingButton = MainButton(self, "manualleveling", _("Manual Leveling"), "manuel-leveling", "co_print_manuel_leveling_screen",2.2, False)
        networkButton = MainButton(self, "network", _("Network"), "network", "co_print_network_setting_screen",2, False)
        inputShaperButton = MainButton(self, "inputshaper2", _("Input Shaper"), "input-shaper", "co_print_input_shaper_screen",2, False)
        cameraButton = MainButton(self, "webcam", _("Camera"), "camera", "co_print_camera_setting_screen",2, False)
        consoleButton = MainButton(self, "console2", _("Console"), "console", "co_print_console_screen",2, False)
        advSettingsButton = MainButton(self, "advsetting", _("Adv. Settings"), "adv-setting", "co_print_advanced_setting_screen",2, False)
        movementButton = MainButton(self, "movement", _("Movement"), "movement", "co_print_movement_setting_screen",2, False)
        #macrosButton = MainButton(self, "macro", ("Macros"), "macros", "system",2, False)
        macrosButton = MainButton(self, "macro", _("Macros"), "macros", "co_print_macros_setting_screen",2, False)

        
        grid = Gtk.Grid()
        grid.set_column_spacing(20)
        grid.set_row_spacing(40)
        grid.set_column_homogeneous(True)
        grid.attach(probeCalibrationButton, 0, 0, 1, 1)
        grid.attach(autoLevelingButton, 1, 0, 1, 1)
        grid.attach(manuelLevelingButton, 2, 0, 1, 1)
        grid.attach(networkButton, 3, 0, 1, 1)
        grid.attach(inputShaperButton, 4, 0, 1, 1)
        grid.attach(cameraButton, 0, 1, 1, 1)
        grid.attach(consoleButton, 1, 1, 1, 1)
        grid.attach(advSettingsButton, 2, 1, 1, 1)
        grid.attach(movementButton, 3, 1, 1, 1)
        grid.attach(macrosButton, 4, 1, 1, 1)
        
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        right_box.pack_start(grid, False, False, 0)
        right_box.set_halign(Gtk.Align.CENTER)
        right_box.set_vexpand(True)
        menu = BottomMenu(self, True)
     
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
      
        page.pack_start(right_box, True, True, 0)
        page.pack_end(menu, False, True, 0)
        
        
        self.content.add(page)

   


