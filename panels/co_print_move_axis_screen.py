import logging
import os
import gi
from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.extrudeheat import ExtrudeHeat
from ks_includes.widgets.infodialog import InfoDialog
from ks_includes.widgets.movebuttonbox import MoveButtonBox
from ks_includes.widgets.zaxis import zAxis
from ks_includes.widgets.keypad_new import KeyPadNew
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf
from ks_includes.screen_panel import ScreenPanel
from ks_includes.widgets.keypad import Keypad

# def create_panel(*args):
#     return CoPrintMoveAxisScreen(*args)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
   

class Panel(ScreenPanel, metaclass=Singleton):

    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        self.grid = self._gtk.HomogeneousGrid()
        self.grid.set_hexpand(True)
        self.grid.set_vexpand(True)


        self.desiredExtruderTemp = -1
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.set_name("x-y-axis-buttons-box")
        
        downIcon = self._gtk.Image("movealt", self._screen.width *.06, self._screen.width *.06)
        upIcon = self._gtk.Image("moveust", self._screen.width *.06, self._screen.width *.06)
        leftIcon = self._gtk.Image("movesol", self._screen.width *.06, self._screen.width *.06)
        rightIcon = self._gtk.Image("movesag", self._screen.width *.06, self._screen.width *.06)
        homeIcon = self._gtk.Image("homing", self._screen.width *.06, self._screen.width *.06)
        motorCloseIcon = self._gtk.Image("motor-close", self._screen.width *.06, self._screen.width *.06)
        
        downButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        downButtonBox.set_name("down-button-box")
        downButton = Gtk.Button(name ="move-grid-buttons")
        downButton.set_image(downIcon)
        downButton.set_always_show_image(True)
        downButton.connect("clicked", self.move, "Y", "-")
        downButtonBox.add(downButton)
        
        upButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        upButtonBox.set_name("up-button-box")
        upButton = Gtk.Button(name ="move-grid-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)
        upButton.connect("clicked", self.move, "Y", "+")
        upButtonBox.add(upButton)
        
        leftButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        leftButtonBox.set_name("left-button-box")
        leftButton = Gtk.Button(name ="move-grid-buttons")
        leftButton.set_image(leftIcon)
        leftButton.set_always_show_image(True)
        leftButton.connect("clicked", self.move, "X", "-")
        leftButtonBox.add(leftButton)

        rightButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        rightButtonBox.set_name("right-button-box")
        rightButton = Gtk.Button(name ="move-grid-buttons")
        rightButton.set_image(rightIcon)
        rightButton.set_always_show_image(True)
        rightButton.connect("clicked", self.move, "X", "+")
        rightButtonBox.add(rightButton)

        homeButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        homeButtonBox.set_name("home-button-box")
        homeButton = Gtk.Button(name ="home-buttons")
        homeButton.set_image(homeIcon)
        homeButton.set_always_show_image(True)
        homeButton.connect("clicked", self.home)
        #homeButton.connect("clicked", self.show_numpad)
        homeButtonBox.add(homeButton)
        
        disableStepperButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        disableStepperButtonBox.set_name("stepper-button-box")
        disableStepperButton = Gtk.Button(name ="move-grid-buttons")
        disableStepperButton.set_image(motorCloseIcon)
        disableStepperButton.set_always_show_image(True)
        disableStepperButton.connect("clicked", self.disable_motors)
        disableStepperButtonBox.add(disableStepperButton)
        
        headLabel = Gtk.Label(_("X Axis (Head)"), name="move-head-label")
        headLabel.set_valign(Gtk.Align.END)
        
        bedLabel = Gtk.Label(_("Y Axis (Bed)"), name="move-head-label")
        bedLabel.set_valign(Gtk.Align.END)
        
        multiButton_grid = Gtk.Grid()
       
        multiButton_grid.set_column_homogeneous(False)
        multiButton_grid.set_valign(Gtk.Align.CENTER)
        multiButton_grid.set_halign(Gtk.Align.CENTER)

        multiButton_grid.attach(leftButtonBox, 0, 2, 1, 1)
        multiButton_grid.attach(upButtonBox, 1, 1, 1, 1)
        multiButton_grid.attach(downButtonBox, 1, 3, 1, 1)
        multiButton_grid.attach(homeButtonBox, 1, 2, 1, 1)
        multiButton_grid.attach(bedLabel, 1, 0, 1, 1)
        multiButton_grid.attach(headLabel, 2, 1, 1, 1)
        multiButton_grid.attach(rightButtonBox, 2, 2, 1, 1)
        multiButton_grid.attach(disableStepperButtonBox, 0, 3, 1, 1)
        
        
        multiButton_grid_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        multiButton_grid_box.set_halign(Gtk.Align.CENTER)
        multiButton_grid_box.set_name("move-page-common-box")
      
        multiButton_grid_box.add(multiButton_grid)
        
        self.distance = 1
        moveButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        moveButtonBox.set_halign(Gtk.Align.CENTER)
        moveButtonBox.set_name("move-page-common-box")
        moveButtons = MoveButtonBox(_("X,Y,Z Hareket Mesafesi (mm)"), 10, 5, 1, 0.1, "move-button", self)
        moveButtonBox.add(moveButtons)
        
        zAxisBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        
        zAxisBox.set_name("move-page-common-box")
        zAxisBox.set_halign(Gtk.Align.CENTER)
        ZAxis = zAxis(self, _("Z Axis"), True)
        zAxisBox.add(ZAxis)
        
        
        self.extruderSwitch = Gtk.Switch(name = "extruder-switch-2")
        self.extruderSwitch.connect("notify::active", self.on_switch_activated, 'extruder')
        self.extruderSwitch.set_hexpand(False)
        extruderLabel = Gtk.Label(_("Preheat For Extrude"), name="move-label")
        extruderLabel.set_max_width_chars(13)
        extruderLabel.set_line_wrap(True)
        extruderLabel.set_justify(Gtk.Justification.CENTER)
        
        switchBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        switchBox.set_halign(Gtk.Align.CENTER)
        switchBox.set_hexpand(False)
        #switchBox.set_name("extrude-switch-box")
        switchBox.pack_start(self.extruderSwitch, False, False, 5)
        switchBox.pack_start(extruderLabel, False, False, 5)
        
        extruderImage = self._gtk.Image("extrr", self._screen.width *.09, self._screen.width *.09)
        switchWithImageBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        switchWithImageBox.add(extruderImage)
        switchWithImageBox.add(switchBox)
        
        
        extrudeBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        extrudeBox.set_valign(Gtk.Align.CENTER)
        extrudeBox.pack_start(switchWithImageBox, False, False, 0)
        
        numPadIcon = self._gtk.Image("calculator", self._screen.width *.04, self._screen.width *.04)
        numPadButton = Gtk.Button(name ="speed-factor-button")
        numPadButton.connect("clicked", self.open_numpad)
        numPadButton.set_image(numPadIcon)
        numPadButton.set_always_show_image(True)
        
        self.extrudeHeatLevel = Gtk.Label("100", name="number-label")
        
        
        numberLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        numberLabelBox.set_valign(Gtk.Align.CENTER)
        numberLabelBox.set_halign(Gtk.Align.CENTER)
        numberLabelBox.set_name("number-label-box")
        numberLabelBox.pack_start(self.extrudeHeatLevel, True, False, 0)
        
        InputBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        InputBox.set_valign(Gtk.Align.CENTER)
        InputBox.pack_start(numberLabelBox, True, True, 0)
        InputBox.pack_end(numPadButton, False, False, 0)
        extrudeBox.pack_start(InputBox, False, False, 0)
        
        Extrude = ExtrudeHeat(self, "", False)
        ExtrudeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ExtrudeBox.pack_start(Extrude, False, False, 0)
        ExtrudeBox.set_halign(Gtk.Align.CENTER)
        
        extrudeBox.pack_start(ExtrudeBox, False, False, 0)
        
        
        extrudeBox_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        extrudeBox_box.set_halign(Gtk.Align.CENTER)
        extrudeBox_box.set_name("move-page-common-box")
        extrudeBox_box.pack_start(extrudeBox, False, False, 0)
        
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.content_box.pack_start(multiButton_grid_box, True, True, 0)
        self.content_box.pack_start(moveButtonBox, True, True, 5)
        self.content_box.pack_start(zAxisBox, True, True, 5)
        self.content_box.pack_start(extrudeBox_box, False, False, 5)
        
        self.main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main.set_vexpand(True)
        self.main.pack_start(self.content_box, False, True, 40)
        self.main.pack_end(BottomMenu(self, True), False, True, 0)
        
        self.grid.attach(self.main, 1, 1, 1, 1)
        self.content.add(self.grid)
        
    def open_numpad(self, widget):
        
        dialog = KeyPadNew(self)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            resp = dialog.resp
            self.extrudeHeatLevel.set_label(resp)
            
            
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
       
        dialog.destroy()
    def close_dialog(self, dialog):
        zero_gcode  = self._printer.data["gcode_move"]["gcode_position"][0]
        zero_homing = self._printer.data["gcode_move"]["homing_origin"][0]

        one_gcode  = self._printer.data["gcode_move"]["gcode_position"][1]
        one_homing = self._printer.data["gcode_move"]["homing_origin"][1]

        two_gcode  = self._printer.data["gcode_move"]["gcode_position"][2]
        two_homing = self._printer.data["gcode_move"]["homing_origin"][2]
        if(zero_gcode + zero_homing == 0 and one_gcode + one_homing == 0 and two_gcode + two_homing == 0):
          dialog.response(Gtk.ResponseType.CANCEL)
          dialog.destroy()
        else:
            return True
    def disable_motors(self, widget):
        
        self._screen._ws.klippy.gcode_script(
            "M18"  # Disable motors
        )        
    def home(self, widget):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.HOME, self.finished)
        self.dialog = InfoDialog(self, _("Printer is returning to the starting position, please wait.."), False)
        self.dialog.get_style_context().add_class("alert-info-dialog")
       
        self.dialog.set_decorated(False)
        self.dialog.set_size_request(0, 0)
        #timer_duration = 1000
        #GLib.timeout_add(timer_duration, self.close_dialog, self.dialog)
        response = self.dialog.run()
       
    def finished(self,asd,a,b):
        self.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.destroy()


    def homexy(self, widget):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.HOME_XY)

    def z_tilt(self, widget):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.Z_TILT)

    def quad_gantry_level(self, widget):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.QUAD_GANTRY_LEVEL)    
    
    def on_switch_activated(self, switch, gparam,a):
        if switch.get_active():
            temp = 200
        else:
            temp = 0

        self.change_extruder_temperature(temp)
    
    
    def change_extruder_temperature(self,temp):
        max_temp = float(self._printer.get_config_section('extruder')['max_temp'])
        if self.validate('extruder', temp, max_temp):
            self._screen._ws.klippy.set_tool_temp(self._printer.get_tool_number('extruder'), temp)
    
    def reset_values(self):
        self.desiredExtruderTemp = -1
    
   
        
    def process_update(self, action, data):
        # if self._printer.state == 'error' or self._printer.state == 'shutdown' or self._printer.state ==  'disconnected':
        #     page_url = 'co_print_home_not_connected_screen'
        #     self._screen.show_panel(page_url, page_url, "Language", 1, False)   
    
        if self._printer.state != 'error' :
             
          
            extruder_array = self._printer.get_temp_store('extruder')
           
            extruder_temp_target = extruder_array['targets'][-1]
            if(self.desiredExtruderTemp == -1):
                self.desiredExtruderTemp = 0
                if(extruder_temp_target >0 ):
                    if(self.extruderSwitch.get_active() == False):
                        self.extruderSwitch.set_active(True)
                else:
                    if(self.extruderSwitch.get_active()):
                        self.extruderSwitch.set_active(False)
              

    def move(self, widget, axis, direction):
        if self._config.get_config()['main'].getboolean(f"invert_{axis.lower()}", False):
            direction = "-" if direction == "+" else "+"

        dist = f"{direction}{self.distance}"
        config_key = "move_speed_z" if axis == "Z" else "move_speed_xy"
        speed = None if self.ks_printer_cfg is None else self.ks_printer_cfg.getint(config_key, None)
        if speed is None:
            speed = self._config.get_config()['main'].getint(config_key, 20)
        speed = 60 * max(1, speed)

        self._screen._ws.klippy.gcode_script(f"{KlippyGcodes.MOVE_RELATIVE}\n{KlippyGcodes.MOVE} {axis}{dist} F{speed}")
        if self._printer.get_stat("gcode_move", "absolute_coordinates"):
            self._screen._ws.klippy.gcode_script("G90")

    def show_numpad(self, widget, device=None):
        

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

    def hide_numpad(self, widget=None):
       
        if self._screen.vertical_mode:
            self.grid.remove_row(1)
            self.grid.attach(self.main, 1, 1, 1, 1)
        else:
            self.grid.remove_column(1)
            self.grid.attach(self.main, 1, 1, 1, 1)
        self.grid.show_all()

    def change_target_temp(self, temp):

        max_temp = int(float(self._printer.get_config_section(self.active_heater)['max_temp']))
        if temp > max_temp:
            self._screen.show_popup_message(_("Can't set above the maximum:") + f' {max_temp}')
            return
        temp = max(temp, 0)
        name = self.active_heater.split()[1] if len(self.active_heater.split()) > 1 else self.active_heater

        if self.active_heater.startswith('extruder'):
            self._screen._ws.klippy.set_tool_temp(self._printer.get_tool_number(self.active_heater), temp)
        elif self.active_heater == "heater_bed":
            self._screen._ws.klippy.set_bed_temp(temp)
        elif self.active_heater.startswith('heater_generic '):
            self._screen._ws.klippy.set_heater_temp(name, temp)
        elif self.active_heater.startswith('temperature_fan '):
            self._screen._ws.klippy.set_temp_fan_temp(name, temp)
        else:
            logging.info(f"Unknown heater: {self.active_heater}")
            self._screen.show_popup_message(_("Unknown Heater") + " " + self.active_heater)
        self._printer.set_dev_stat(self.active_heater, "target", temp)

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
    
    def on_button_clicked(self, widget, value):
            # Mevcut değeri alın
            #current_value = float(self.entry.get_text())
            current_value = float(self.printer._printer.data["gcode_move"]["homing_origin"][2])
            # Yeni değeri hesaplayın
            new_value = current_value + value
            direction = '-'
            if value > 0:
                 direction = '+'
                
            self.printer._screen._ws.klippy.gcode_script(f"SET_GCODE_OFFSET Z_ADJUST={direction}{abs(value)} MOVE=1")
            
            
            # Yeni değeri entry'ye ayarlayın
            self.entry.set_text('{:.2f}'.format(new_value))
   
    
  