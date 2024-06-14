import logging
import os
import gi
import contextlib
from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.kalibrationinfodialog import KalibrationInfoDialog
from ks_includes.widgets.zaxishorizontalcalibration import zAxisHorizontalCalibration
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintProbeCalibrationScreen(*args)


# class CoPrintProbeCalibrationScreen(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        menu = BottomMenu(self, False)
        
        self.labels['probeImage'] = self._gtk.Image("probcalibre", self._screen.width / 2.25, self._screen.height / 1.80)
        # self.labels['probeImage'].get_style_context().add_class("thumbnail")
        
        zOffsetDistanceLabel = Gtk.Label(_("Z Offset Distance") + ":", name="zoffset-distance-label")
        distanceLabel = Gtk.Label("4.325" + _("mm"), name="distance-label")
        zOffsetLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        zOffsetLabelBox.set_halign(Gtk.Align.CENTER)
        zOffsetLabelBox.pack_start(zOffsetDistanceLabel, True, True, 0)
        zOffsetLabelBox.pack_start(distanceLabel, True, True, 0)
        
        self.startButton = Gtk.Button(_('Start'),name ="probe-calibration-start-button")
        self.startButton.connect("clicked", self.open_info_dialog)
        startButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        startButtonBox.set_halign(Gtk.Align.CENTER)
        startButtonBox.pack_start(self.startButton, False, False, 0)
        
        probeCalibrationLabel = Gtk.Label(_("Prob Calibration"), name="probe-calibration-label")
        probeCalibrationLabel.set_justify(Gtk.Justification.LEFT)
        probeCalibrationBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        probeCalibrationBox.pack_start(probeCalibrationLabel, False, False, 30)
        
        zoffset_calibration_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        zoffset_calibration_box.set_valign(Gtk.Align.CENTER)
        zoffset_calibration_box.pack_start(self.labels['probeImage'], True, True, 0)
        #zoffset_calibration_box.pack_start(zOffsetLabelBox, False, False, 0)
        
        
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        left_box.pack_start(probeCalibrationBox, False, False, 0)
        left_box.pack_start(zoffset_calibration_box, True, True, 0)
        left_box.pack_end(startButtonBox, False, False, 20)

        changeOffsetButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        changeOffsetButtonBox.set_spacing(-10)
    
        self.OffsetConstant = 0.5
        
        
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
        
        
        
        zAxis = zAxisHorizontalCalibration(self, True)
        
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
        
        self.okButton = Gtk.Button(_('Ok'),name ="probe-calibration-start-button")
        self.okButton.connect("clicked", self.accept)
        
        okButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        okButtonBox.set_halign(Gtk.Align.CENTER)
        okButtonBox.pack_start(self.okButton, False, False, 0)
        
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        right_box.pack_start(changeOffsetBox, False, False, 35)
        right_box.pack_start(zOffsetBox, False, False, 20)
        right_box.pack_end(okButtonBox, False, False, 20)
        
        
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main_box.set_vexpand(True)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.pack_start(left_box, False, False, 0)
        main_box.pack_start(right_box, False, False, 0)
        
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(main_box, True, True, 0)
        page.pack_end(menu, False, True, 0)
        

        
        self.content.add(page)

    def open_info_dialog(self, widget):
        
       
        
        #timer_duration = 3000
        #GLib.timeout_add(timer_duration, self.close_dialog, dialog)
        GLib.idle_add(self.start_calibration)
        
        
       
        #dialog.destroy()    
        
    def close_dialog(self, dialog):
        
        dialog.response(Gtk.ResponseType.CANCEL)
        dialog.destroy()

    def process_update(self, action, data):
        if action == "notify_busy":
            #self.process_busy(data)
            return
        if action == "notify_status_update":
            if self._printer.get_stat("toolhead", "homed_axes") != "xyz":
               # self.widgets['zposition'].set_text("Z: ?")
                print("Z: ?")
            elif "gcode_move" in data and "gcode_position" in data['gcode_move']:
                #self.update_position(data['gcode_move']['gcode_position'])
                print(data['gcode_move']['gcode_position'])
        elif action == "notify_gcode_response":
            data = data.lower()
            if "unknown" in data:
                #self.buttons_not_calibrating()
                logging.info(data)
            #elif "save_config" in data:
                #self.buttons_not_calibrating()
            elif "out of range" in data:
                self._screen.show_popup_message(data)
                #self.buttons_not_calibrating()
                logging.info(data)
            elif "fail" in data and "use testz" in data:
                self._screen.show_popup_message(_("Failed, adjust position first"))
                #self.buttons_not_calibrating()
                logging.info(data)
            #elif "use testz" in data or "use abort" in data or "z position" in data:
                #self.buttons_calibrating()
        return
                    
    def start_calibration(self):
        self.zoffset.set_label('{:.3f}'.format(0))
        functions = []
        self.probe = self._printer.get_probe()
        if self._printer.config_section_exists("stepper_z") \
                and not self._printer.get_config_section("stepper_z")['endstop_pin'].startswith("probe"):
            method = "endstop"
            functions.append("endstop")
        if self.probe:
           
            method = "probe"
            functions.append("probe")
        if self._printer.config_section_exists("bed_mesh") and "probe" not in functions:
            # This is used to do a manual bed mesh if there is no probe
            
            method = "mesh"
            functions.append("mesh")
        if "delta" in self._printer.get_config_section("printer")['kinematics']:
            if "probe" in functions:
                
                method = "delta"
                functions.append("delta")
            # Since probes may not be accturate enough for deltas, always show the manual method
           
            method = "delta_manual"
            functions.append("delta_manual")

        #self.labels['popover'].popdown()
        if self._printer.get_stat("toolhead", "homed_axes") != "xyz":
            self.home()

        if method == "probe":
            #self._move_to_position()
            self._screen._ws.klippy.gcode_script(KlippyGcodes.PROBE_CALIBRATE)
        elif method == "mesh":
            self._screen._ws.klippy.gcode_script("BED_MESH_CALIBRATE")
        elif method == "delta":
            self._screen._ws.klippy.gcode_script("DELTA_CALIBRATE")
        elif method == "delta_manual":
            self._screen._ws.klippy.gcode_script("DELTA_CALIBRATE METHOD=manual")
        elif method == "endstop":
            self._screen._ws.klippy.gcode_script(KlippyGcodes.Z_ENDSTOP_CALIBRATE)

    def _move_to_position(self, zhop):
        x_position = y_position = None
        speed = None
        # Get position from config
        if self.ks_printer_cfg is not None:
            x_position = self.ks_printer_cfg.getfloat("calibrate_x_position", None)
            y_position = self.ks_printer_cfg.getfloat("calibrate_y_position", None)
        elif 'z_calibrate_position' in self._config.get_config():
            # OLD global way, this should be deprecated
            x_position = self._config.get_config()['z_calibrate_position'].getfloat("calibrate_x_position", None)
            y_position = self._config.get_config()['z_calibrate_position'].getfloat("calibrate_y_position", None)

        if self.probe:
            #if "sample_retract_dist" in self.probe:
                #z_hop = self.probe['sample_retract_dist']
            if "speed" in self.probe:
                speed = self.probe['speed']

        # Use safe_z_home position
        if "safe_z_home" in self._printer.get_config_section_list():
            safe_z = self._printer.get_config_section("safe_z_home")
            safe_z_xy = safe_z['home_xy_position']
            safe_z_xy = [str(i.strip()) for i in safe_z_xy.split(',')]
            if x_position is None:
                x_position = float(safe_z_xy[0])
                logging.debug(f"Using safe_z x:{x_position}")
            if y_position is None:
                y_position = float(safe_z_xy[1])
                logging.debug(f"Using safe_z y:{y_position}")
            #if 'z_hop' in safe_z:
                #z_hop = safe_z['z_hop']
            if 'z_hop_speed' in safe_z:
                speed = safe_z['z_hop_speed']

        speed = 15 if speed is None else speed
        #z_hop = 5 if z_hop is None else z_hop
       
        self._screen._ws.klippy.gcode_script(f"TESTZ Z={zhop}")
        #self._screen._ws.klippy.gcode_script(f"G91\nG0 Z{zhop} F{float(speed) * 60}")
       # if self._printer.get_stat("gcode_move", "absolute_coordinates"):
        #    self._screen._ws.klippy.gcode_script("G90")

        if x_position is not None and y_position is not None:
            logging.debug(f"Configured probing position X: {x_position} Y: {y_position}")
           # self._screen._ws.klippy.gcode_script(f'G0 X{x_position} Y{y_position} F3000')
        elif "delta" in self._printer.get_config_section("printer")['kinematics']:
            logging.info("Detected delta kinematics calibrating at 0,0")
           # self._screen._ws.klippy.gcode_script('G0 X0 Y0 F3000')
        else:
            self._calculate_position()

    def _calculate_position(self):
        logging.debug("Position not configured, probing the middle of the bed")
        try:
            xmax = float(self._printer.get_config_section("stepper_x")['position_max'])
            ymax = float(self._printer.get_config_section("stepper_y")['position_max'])
        except KeyError:
            logging.error("Couldn't get max position from stepper_x and stepper_y")
            return
        x_position = xmax / 2
        y_position = ymax / 2
        logging.info(f"Center position X:{x_position} Y:{y_position}")

        # Find probe offset
        x_offset = y_offset = None
        if self.probe:
            if "x_offset" in self.probe:
                x_offset = float(self.probe['x_offset'])
            if "y_offset" in self.probe:
                y_offset = float(self.probe['y_offset'])
        logging.info(f"Offset X:{x_offset} Y:{y_offset}")
        if x_offset is not None:
            x_position = x_position - x_offset
        if y_offset is not None:
            y_position = y_position - y_offset

        logging.info(f"Moving to X:{x_position} Y:{y_position}")
        self._screen._ws.klippy.gcode_script(f'G0 X{x_position} Y{y_position} F3000')

    def accept(self, widget):
        logging.info("Accepting Z position")
        self._screen._ws.klippy.gcode_script(KlippyGcodes.ACCEPT)
        self.save_config()


    def save_config(self):

        script = {"script": "SAVE_CONFIG"}
        self._screen._confirm_send_action(
            None,
            _("Save configuration?") + "\n\n" + _("Klipper will reboot"),
            "printer.gcode.script",
            script
        )

    def home(self):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.HOME, self.finished)
        self.dialog = KalibrationInfoDialog(self)
        self.dialog.get_style_context().add_class("info-dialog")
        self.dialog.set_decorated(False)
        self.dialog.set_size_request(0, 0)
        #timer_duration = 1000
        #GLib.timeout_add(timer_duration, self.close_dialog, self.dialog)
        response = self.dialog.run()
    def finished(self,asd,a,b):
        self.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.destroy()


    def chanceOffset(self,widget,  number):
        
        self.buttons[f"{self.OffsetConstant}"].get_style_context().remove_class("probe-change-offset-button-active")
        self.buttons[f"{number}"].get_style_context().add_class("probe-change-offset-button-active")
        self.OffsetConstant = number

