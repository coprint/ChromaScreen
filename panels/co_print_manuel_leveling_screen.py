import logging
import os
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.infodialog import InfoDialog
from ks_includes.widgets.zaxishorizontal import zAxisHorizontal
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintManuelLevelingScreen(*args)


# class CoPrintManuelLevelingScreen(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        menu = BottomMenu(self, False)
        
        #tabla = self._gtk.Image("tabla1", self._screen.width *.35, self._screen.width *.35)
        tabla = self._gtk.Image("tabla1", self._screen.width *.37, self._screen.width *.37)
        
        self.autoOneButton = Gtk.Button('1',name ="manuel-leveling-buttons")
        self.autoOneButton.connect("clicked", self.manuel_level, 1)
        autoOneButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        autoOneButtonBox.set_halign(Gtk.Align.CENTER)
        autoOneButtonBox.pack_start(self.autoOneButton, False, False, 0)
        
        self.autoTwoButton = Gtk.Button('2',name ="manuel-leveling-buttons")
        self.autoTwoButton.connect("clicked", self.manuel_level, 2)
        autoTwoButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        autoTwoButtonBox.set_halign(Gtk.Align.CENTER)
        autoTwoButtonBox.pack_start(self.autoTwoButton, False, False, 0)
        
        self.autoThreeButton = Gtk.Button('3',name ="manuel-leveling-buttons")
        self.autoThreeButton.connect("clicked", self.manuel_level, 3)
        autoThreeButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        autoThreeButtonBox.set_halign(Gtk.Align.CENTER)
        autoThreeButtonBox.set_valign(Gtk.Align.CENTER)
        autoThreeButtonBox.pack_start(self.autoThreeButton, False, False, 0)
        
        self.autoFourButton = Gtk.Button('4',name ="manuel-leveling-buttons")
        self.autoFourButton.connect("clicked", self.manuel_level, 4)
        autoFourButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        autoFourButtonBox.set_halign(Gtk.Align.CENTER)
        autoFourButtonBox.pack_start(self.autoFourButton, False, False, 0)
        
        
        fixed = Gtk.Fixed()
        fixed.set_valign(Gtk.Align.START)
        fixed.set_halign(Gtk.Align.START)
        fixed.put(tabla, 5, 5)
        fixed.put(autoThreeButtonBox, 8, 4)
        fixed.put(autoFourButtonBox, 305, 4)
        fixed.put(autoOneButtonBox, 8, 305)
        fixed.put(autoTwoButtonBox, 305, 305)
      
        fixedBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        fixedBox.pack_start(fixed, False, False, 0)
        
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        left_box.set_name("manuel-fixed-box")
        left_box.pack_start(fixedBox, False, False, 0)
       
        changeOffsetButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        changeOffsetButtonBox.set_spacing(-13)
    
        self.buttons = {"0.01": Gtk.Button("0.01", name ="probe-change-offset-button"),
                        "0.1": Gtk.Button("0.1", name ="probe-change-offset-button"),
                        "0.5": Gtk.Button("0.5", name ="probe-change-offset-button"),
                        "1": Gtk.Button("1", name ="probe-change-offset-button"),
                        "2": Gtk.Button("2", name ="probe-change-offset-button")
        }

        self.OffsetConstant = 0.5
        self.buttons[f"{0.01}"].connect("clicked", self.chanceOffset, 0.01)
        self.buttons[f"{0.1}"].connect("clicked", self.chanceOffset, 0.1)
        self.buttons[f"{0.5}"].connect("clicked", self.chanceOffset, 0.5)
        self.buttons[f"{1}"].connect("clicked", self.chanceOffset, 1)
        self.buttons[f"{2}"].connect("clicked", self.chanceOffset, 2)
        
        self.buttons[f"{0.5}"].get_style_context().add_class("probe-change-offset-button-active")
        
        

        changeOffsetButtonBox.pack_start(self.buttons[f"{0.01}"], True, True, 0)
        changeOffsetButtonBox.pack_start(self.buttons[f"{0.1}"], True, True, 0)
        changeOffsetButtonBox.pack_start(self.buttons[f"{0.5}"], True, True, 0)
        changeOffsetButtonBox.pack_start(self.buttons[f"{1}"], True, True, 0)
        changeOffsetButtonBox.pack_start(self.buttons[f"{2}"], True, True, 0)
        
        changeOffsetLabel = Gtk.Label(_("Change Offset"), name="probe-calibration-label")
        changeOffsetLabel.set_justify(Gtk.Justification.LEFT)
        changeOffsetLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        changeOffsetLabelBox.pack_start(changeOffsetLabel, False, False, 0)
        
        changeOffsetBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        changeOffsetBox.pack_start(changeOffsetLabelBox, False, False, 10)
        changeOffsetBox.pack_start(changeOffsetButtonBox, False, False, 20)
        
        zAxis = zAxisHorizontal(self, True)
        
        zOffsetLabel = Gtk.Label(_("Z Offset"))
        
        self.zoffset = Gtk.Label("0", name="number-label")
        numberLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        numberLabelBox.set_valign(Gtk.Align.CENTER)
        numberLabelBox.set_halign(Gtk.Align.CENTER)
        numberLabelBox.set_name("probe-calibration-label-box")
        numberLabelBox.add(self.zoffset)
        
        zOffsetBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        zOffsetBox.set_name("probe-zoffset-box")
        zOffsetBox.set_valign(Gtk.Align.CENTER)
        zOffsetBox.set_halign(Gtk.Align.CENTER)
        zOffsetBox.pack_start(zAxis, False, False, 0)
        zOffsetBox.pack_start(zOffsetLabel, False, False, 40)
        zOffsetBox.pack_start(numberLabelBox, False, False, 0)
        
        zCalibrationTitle = Gtk.Label(_("Z Calibration Steps"))
        zCalibrationTitle.set_justify(Gtk.Justification.LEFT)
        zCalibrationTitleBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        zCalibrationTitleBox.set_name("z-calibration-title-box")
        zCalibrationTitleBox.pack_start(zCalibrationTitle, False, False, 0)
        
        zCalibrationContent = Gtk.Label(_("First, tighten the tension screws to their maximum value. Then, for the first step, make a height adjustment using paper."), name="z-calibration-content-label")
        zCalibrationContent.set_max_width_chars(50)
        zCalibrationContent.set_line_wrap(True)
        zCalibrationContent.set_justify(Gtk.Justification.LEFT)
        zCalibrationContentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        zCalibrationContentBox.set_name("z-calibration-content-box")
        zCalibrationContentBox.pack_start(zCalibrationContent, False, False, 0)
        
        self.saveButton = Gtk.Button(_('Save Settings'),name ="save-settings-button")
        self.saveButton.connect("clicked", self.save)
        saveButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        saveButtonBox.set_halign(Gtk.Align.CENTER)
        saveButtonBox.pack_start(self.saveButton, False, False, 0)
        
        zCalibrationBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        zCalibrationBox.set_name("z-calibration-box")
        zCalibrationBox.pack_start(zCalibrationTitleBox, False, False, 0)
        zCalibrationBox.pack_start(zCalibrationContentBox, False, False, 0)
        zCalibrationBox.pack_start(saveButtonBox, False, False, 0)
        
        self.right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.right_box.pack_start(zOffsetBox, False, False, 0)
        self.right_box.pack_start(changeOffsetBox, False, False, 0)
        self.right_box.pack_start(zCalibrationBox, True, True, 0)
        
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        main_box.set_vexpand(True)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.pack_start(left_box, False, True, 5)
        main_box.pack_start(self.right_box, False, True, 0)
   
        
        self.page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.page.pack_start(main_box, False, True, 0)
        self.page.pack_end(menu, False, True, 0)
        
        self.content.add(self.page)
    

    def manuel_level(self, widget, value):
        self.dialog = InfoDialog(self, _("This Feature is coming in the next update, thank you for using ChromaScreen."), True)
        self.dialog.get_style_context().add_class("alert-info-dialog")
        # gcode_script = "go_screw_" + str(value)


        # self._screen._ws.klippy.gcode_script(gcode_script, self.finished)
        # self.dialog = InfoDialog(self, _("Processing, Please Wait.."), False)
        # self.dialog.get_style_context().add_class("alert-info-dialog")
       
        # self.dialog.set_decorated(False)
        # self.dialog.set_size_request(0, 0)
        # #timer_duration = 1000
        # #GLib.timeout_add(timer_duration, self.close_dialog, self.dialog)
        # response = self.dialog.run()

    def finished(self,asd,a,b):
        self.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.destroy()

    def save(self,asd):
        script = {"script": "SAVE_CONFIG"}
        self._screen._confirm_send_action(
            None,
            _("Save configuration?") + "\n\n" + _("Klipper will reboot"),
            "printer.gcode.script",
            script
        )
   
    def process_update(self, action, data):

        # if self._printer.state == 'error' or self._printer.state == 'shutdown' or self._printer.state ==  'disconnected':
        #     page_url = 'co_print_home_not_connected_screen'
        #     self._screen.show_panel(page_url, page_url, "Language", 1, False)    

        zoffset = float(self._printer.data["gcode_move"]["homing_origin"][2])
        if self.zoffset.get_label() != '{:.3f}'.format(zoffset):
                    self.zoffset.set_label('{:.3f}'.format(zoffset))
    def chanceOffset(self,widget,  number):
        
        self.buttons[f"{self.OffsetConstant}"].get_style_context().remove_class("probe-change-offset-button-active")
        self.buttons[f"{number}"].get_style_context().add_class("probe-change-offset-button-active")
        self.OffsetConstant = number


    