import logging
from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from math import pi, sqrt
from ks_includes.widgets.counterinputfloat import CounterInputFloat
from ks_includes.widgets.initheader import InitHeader
from ks_includes.widgets.keypad import Keypad
from ks_includes.widgets.keypad_new import KeyPadNew
from ks_includes.widgets.percentagefactor import PercentageFactor
from ks_includes.widgets.progressbar import ProgressBar
from ks_includes.widgets.zoffset import zOffset
from ks_includes.widgets.counterinput import CounterInput
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf
from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintPrintingScreen(*args)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
   
# class CoPrintPrintingScreen(ScreenPanel, metaclass=Singleton):
class Panel(ScreenPanel, metaclass=Singleton):
    extruderChanged = False
    def __init__(self, screen, title):
        super().__init__(screen, title)        
        self.fanSpeed_newValue = 0
        self.speedFactor_newValue = 0
        self.extrusionFactor_newValue = 0
        self.ExtruderMax_temp = 0
        self.HeaterBedMax_temp = 0
        self.startIndex = 1
        self.labels['file'] = Gtk.Label(_("Printing File") + " ")
        self.labels['file'].get_style_context().add_class("printing-filename")
        self.labels['file'].set_hexpand(True)
        self.labels['status'] = Gtk.Label(_("Estimated Time") + ": " + "-") 
        self.labels['status'].get_style_context().add_class("printing-status")
     
        self.filename = ''        
        self.file_metadata = self.fans = {}
        self.speed_factor = 1
        self.fan_spped = 1
        self.extrude_factor = 0
        self.zoffset = 0
        self.pressure_advance = ""
        self.smooth_time = ""
        self.pixbuf = ""
        # self.label1 = Gtk.Label("")
        # self.label2 = Gtk.Label("")
        # self.label3 = Gtk.Label("")
        # self.label4 = Gtk.Label("")
        # self.label5 = Gtk.Label("")
        # self.label6 = Gtk.Label("")
        # self.label7 = Gtk.Label("")
        # self.label8 = Gtk.Label("")
        # self.label9 = Gtk.Label("")
        # labelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # labelBox.pack_start(self.label3, True, True, 0)
        # labelBox.pack_start(self.label4, True, True, 0)
        # labelBox.pack_start(self.label5, True, True, 0)
        # labelBox.pack_start(self.label6, True, True, 0)
        # labelBox.pack_start(self.label7, True, True, 0)
        # labelBox.pack_start(self.label8, True, True, 0)
        # labelBox.pack_start(self.label9, True, True, 0)
        ''' left '''
        self.labels['thumbnail'] = self._gtk.Image(self.pixbuf, self._screen.width / 6, self._screen.height / 2.7)
        self.labels['thumbnail'].get_style_context().add_class("thumbnail")
        
        self.heatedBed = ProgressBar(self, "0.0° / 0.0°", "tablaicon", 0.0, "progress-bar-extruder-yellow", self.change_bed_temperature_pre)
        heatedBed_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        heatedBed_box.set_name("heatedBed_box")
        heatedBed_box.pack_start(self.heatedBed, False, False, 0)
        
        self.extruder = ProgressBar(self, "0.0° / 0.0°", "extrudericon", 0.0, "progress-bar-extruder-blue", self.change_extruder_temperature_pre)
        extruder_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        extruder_box.set_name("heatedBed_box")
        extruder_box.pack_start(self.extruder, False, False, 0)
        
        self.connectedExtruder = Gtk.Label("Extruder 1", name="extruder-label")
        self.connectedExtruder.set_halign(Gtk.Align.START)
        extruder_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        extruder_main_box.set_valign(Gtk.Align.START)
        extruder_main_box.add(self.connectedExtruder)
        extruder_main_box.add(extruder_box)

        heatedBedLabel = Gtk.Label(_("Heated Bed"), name="extruder-label")
        heatedBedLabel.set_halign(Gtk.Align.START)
        heatedBed_main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        heatedBed_main_box.set_valign(Gtk.Align.START)
        heatedBed_main_box.add(heatedBedLabel)
        heatedBed_main_box.add(heatedBed_box)

        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        left_box.set_name("printing-screen-left-box")
        left_box.pack_start(self.labels['thumbnail'], False, False, 0)
        left_box.pack_start(extruder_main_box, False, False, 0)
        left_box.pack_start(heatedBed_main_box, False, False, 0)
        ''''''
        self.buttons = {}
        self.create_buttons()
        for button in self.buttons: 
            self.buttons[button].set_halign(Gtk.Align.START)
            self.buttons[button].set_valign(Gtk.Align.START)
          
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.button_pause_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.button_pause_box.set_name("pause-cancel-button-box")
        if self._printer.state == 'printing':
            self.button_pause_box.add(self.buttons['pause'])
        elif self._printer.state == 'paused':
            self.button_pause_box.add(self.buttons['pause'])
        self.button_pause_box.hide()
        
        button_cancel_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        button_cancel_box.set_name("pause-cancel-button-box")
        button_cancel_box.add(self.buttons['cancel'])
        button_box.pack_end(self.button_pause_box, True, True, 0)
        button_box.pack_end(button_cancel_box, True, True, 10)
        button_box.set_halign(Gtk.Align.END)
        
        fi_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing= 10)
        
        fi_box.pack_start(self.labels['file'], True, True, 0)
        fi_box.pack_start(self.labels['status'], True, True, 0)
        self.labels['file'].set_halign(Gtk.Align.START)
        self.labels['status'].set_halign(Gtk.Align.START)
        
        rightInfo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        rightInfo_box.set_name("printing-right-info-box")
        rightInfo_box.pack_start(fi_box, False, True, 0)
        rightInfo_box.pack_end(button_box, False, True, 0)
        rightInfo_box.set_valign(Gtk.Align.CENTER)
        
        self.scale_printProgress = Gtk.ProgressBar(name ="progress-bar-print")
        self.scale_printProgress.set_fraction(0.0)
        self.scale_printProgress.set_show_text(False)
        self.scale_printProgress.set_hexpand(True) 

        self.zoffset_widget = zOffset(self)
        self.zoffset_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.zoffset_box.set_name("zoffset-box")
        self.zoffset_box.pack_start(self.zoffset_widget, True, False, 0)
        
        changeOffsetButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        changeOffsetButtonBox.set_spacing(-13)
    
       

        self.buttonss = {"0.005": Gtk.Button("0.005", name ="change-offset-button"),
                        "0.01": Gtk.Button("0.01", name ="change-offset-button"),
                        "0.025": Gtk.Button("0.025", name ="change-offset-button"),
                        "0.05": Gtk.Button("0.05", name ="change-offset-button"),
        }

        self.OffsetConstant = 0.01
        self.buttonss[f"{0.005}"].connect("clicked", self.chanceOffset, 0.005)
        self.buttonss[f"{0.01}"].connect("clicked", self.chanceOffset, 0.01)
        self.buttonss[f"{0.025}"].connect("clicked", self.chanceOffset, 0.025)
        self.buttonss[f"{0.05}"].connect("clicked", self.chanceOffset, 0.05)
        
        self.buttonss[f"{0.01}"].get_style_context().add_class("change-offset-button-active")
        
        changeOffsetButtonBox.pack_start(self.buttonss[f"{0.005}"], True, True, 0)
        changeOffsetButtonBox.pack_start(self.buttonss[f"{0.01}"], True, True, 0)
        changeOffsetButtonBox.pack_start(self.buttonss[f"{0.025}"], True, True, 0)
        changeOffsetButtonBox.pack_start(self.buttonss[f"{0.05}"], True, True, 0)
        
        changeOffsetLabel = Gtk.Label(_("Change Offset"), name="probe-calibration-label")
        changeOffsetLabel.set_justify(Gtk.Justification.LEFT)
        changeOffsetLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        changeOffsetLabelBox.pack_start(changeOffsetLabel, False, False, 0)
        changeOffsetBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        changeOffsetBox.pack_start(changeOffsetLabelBox, False, False, 0)
        changeOffsetBox.pack_end(changeOffsetButtonBox, False, False, 0)
        self.zoffset_box.pack_start(changeOffsetBox, False, False, 0)
        self.separatorFirst = Gtk.HSeparator()
        self.speedFactor_widget = PercentageFactor(self, "hiz", ("Speed Factor"),900, 1, 'speedFactor')
        self.speedFactor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.speedFactor_box.set_name("zoffset-box")
        self.speedFactor_box.set_valign(Gtk.Align.CENTER)
        self.speedFactor_box.set_halign(Gtk.Align.CENTER)
        self.speedFactor_box.pack_start(self.speedFactor_widget, True, False, 0)
        self.speedFactor_widget.updateValue(100,'')
        self.firstPageBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.firstPageBox.set_name("zoffset-box")
        self.firstPageBox.pack_start(self.zoffset_box, False, False, 0)
        #self.firstPageBox.pack_start(self.separatorFirst, True, False, 0)
        self.firstPageBox.pack_start(self.speedFactor_box, False, False, 0)
        #------------------
        self.pressureAdvanceInput = CounterInputFloat(self, ("s"), ("Pressure Advance"), self.pressure_advance, "SET_PRESSURE_ADVANCE EXTRUDER=extruder ADVANCE=", 0.001)
        self.smoothTimeInput = CounterInputFloat(self, ("s"), ("Smooth Time"), self.smooth_time, "SET_PRESSURE_ADVANCE EXTRUDER=extruder SMOOTH_TIME=", 0.01)
        pressure_smooth_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        pressure_smooth_box.set_valign(Gtk.Align.CENTER)
        pressure_smooth_box.pack_start(self.pressureAdvanceInput, True, True, 0)

        pressure_smooth_box.pack_end(self.smoothTimeInput, True, True, 0)
        
        separator = Gtk.HSeparator()
        separatorsecond = Gtk.HSeparator()
        self.extrusionFactor_widget = PercentageFactor(self, "extrudericon", ("Extrusion Factor"),200, 1, 'extrusionFactor')
        self.extrusionFactor_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.extrusionFactor_box.set_name("zoffset-box")
        self.extrusionFactor_box.pack_start(self.extrusionFactor_widget, True, False, 0)
        self.extrusionFactor_box.pack_start(separator, True, False, 0)
        #self.extrusionFactor_box.pack_start(pressure_smooth_box, True, False, 0)
        #extrusionFactor_box.pack_start(separatorsecond, True, False, 0)
        #extrusionFactor_box.pack_start(filament_extrusion_box, True, False, 0)
        
        self.fanSpeed_widget = PercentageFactor(self, "fanayari", ("Fan Speed"),100,0, 'fan')
        self.fanSpeed_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.fanSpeed_box.set_name("zoffset-box")
        self.fanSpeed_box.pack_start(self.fanSpeed_widget, True, False, 0)
        self.extrusionFactor_box.pack_start(self.fanSpeed_box, True, False, 0)
        
        machineLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        machineImage = self._gtk.Image("motor", self._screen.width *.03, self._screen.width *.03)
        machineLabel = Gtk.Label(("Machine"), name="zoffset-label")
        machineLabelBox.pack_start(machineImage, True, False, 0)
        machineLabelBox.pack_start(machineLabel, True, False, 0)
        machineLabelBox.set_valign(Gtk.Align.START)
        machineLabelBox.set_halign(Gtk.Align.START) 
        
        machineSeparatorFirst = Gtk.HSeparator()
        
        self.velocityInput = CounterInput(self, ("mm/s"), ("Velocity"), "0", "SET_VELOCITY_LIMIT VELOCITY=", 5)
        self.squareCornerInput = CounterInputFloat(self, ("mm/s"), ("Square Corner"), "0", "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=", 0.1)
        velocity_square_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        velocity_square_box.set_valign(Gtk.Align.CENTER)
        velocity_square_box.pack_start(self.velocityInput, True, True, 0)
        velocity_square_box.pack_end(self.squareCornerInput, True, True, 0)
        
        machineSeparatorSecond = Gtk.HSeparator()
        self.acceleration = CounterInput(self, ("mm/s"), ("Acceleration"), "0", "SET_VELOCITY_LIMIT ACCEL=", 100)
        self.maxAcceltoDecel = CounterInput(self, ("mm/s"), ("Min. Cruise Ratio"), "0", "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=", 100)
        acceleration_maxAccel_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        acceleration_maxAccel_box.set_valign(Gtk.Align.CENTER)
        acceleration_maxAccel_box.pack_start(self.acceleration, True, True, 0)
        acceleration_maxAccel_box.pack_end(self.maxAcceltoDecel, True, True, 0)
        
        self.machine_Box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.machine_Box.pack_start(machineLabelBox, True, False, 0)
        self.machine_Box.pack_start(machineSeparatorFirst, True, False, 0)
        self.machine_Box.pack_start(velocity_square_box, True, False, 0)
        self.machine_Box.pack_start(machineSeparatorSecond, True, False, 0)
        self.machine_Box.pack_start(acceleration_maxAccel_box, True, False, 0)
        self.machine_Box.set_name("zoffset-box") 
        filamentIcon = self._gtk.Image("paintPalette", self._screen.width *.04, self._screen.width *.04)
        filamentLabel = Gtk.Label(("Filament Change Count"))
        filametSeparatorFirst = Gtk.HSeparator()
        filametSeparatorSecond = Gtk.HSeparator()
        self.filamentNumberLabel = Gtk.Label("200", name="percentage-factor-label")
        filamentNumberLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        filamentNumberLabelBox.set_valign(Gtk.Align.CENTER)
        filamentNumberLabelBox.set_halign(Gtk.Align.CENTER)
        filamentNumberLabelBox.set_name("percentage-factor-label-box")
        filamentNumberLabelBox.add(self.filamentNumberLabel)
        filamentChangeContentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        filamentChangeContentBox.set_name("filament-change-content-box")
        filamentChangeContentBox.pack_start(filamentIcon, False, False, 0)
        filamentChangeContentBox.pack_start(filamentLabel, False, False, 0)
        filamentChangeContentBox.pack_end(filamentNumberLabelBox, False, False, 0)
        filametChangeCountBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        filametChangeCountBox.pack_start(filametSeparatorFirst, False, False, 0)
        filametChangeCountBox.pack_start(filamentChangeContentBox, False, False, 0)
        filametChangeCountBox.pack_start(filametSeparatorSecond, False, False, 0)
        releaseFilamentButton = Gtk.Button(("Release Filament"),name ="filament-button")
        holdFilamentButton = Gtk.Button(("Hold Filament"),name ="filament-button")
        changeFilamentButton = Gtk.Button(("Change Filament Count"),name ="filament-button")
        filamentButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        filamentButtonBox.set_hexpand(True)
        filamentButtonBox.pack_start(releaseFilamentButton, False, False, 0)
        filamentButtonBox.pack_start(holdFilamentButton, True, False, 0)
        filamentButtonBox.pack_end(changeFilamentButton, False, False, 0)
        gridBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        gridBox.set_name("printing-grid-box")
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.set_valign(Gtk.Align.CENTER)
        # gridBox.add(zoffset_box)
        # gridBox.add(speedFactor_box)
        gridBox.add(filametChangeCountBox)
        gridBox.add(filamentButtonBox)
        #gridBox.add(self.extrusionFactor_box)
        #gridBox.add(machine_Box)
        #gridBox.add(self.fanSpeed_box)
        nextIcon = self._gtk.Image("forward-arrow", 30, 30)
        self.nextButton = Gtk.Button(name ="prev-next-button")
        self.nextButton.add(nextIcon)
        self.nextButton.connect("clicked", self.show_next_page)
        self.nextButton.set_always_show_image (True)   
        nextButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        nextButtonBox.pack_start(self.nextButton, False, False, 0)
        prevIcon = self._gtk.Image("back-arrow", 30, 30)
        self.prevButton = Gtk.Button(name ="prev-next-button")
        self.prevButton.add(prevIcon)
        self.prevButton.connect("clicked", self.show_prev_page)
        self.prevButton.set_always_show_image (True) 
        prevButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        prevButtonBox.pack_start(self.prevButton, False, False, 0)
        self.selectableBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.selectableBox.set_name("zoffset-with-speed-factor-box")
        self.selectableBox.pack_start(self.firstPageBox, False, False, 0)
        #self.selectableBox.pack_start(self.separatorFirst, True, False, 0)
        #self.selectableBox.pack_start(self.speedFactor_box, False, False, 0)
        #gridBox.add(labelBox)
        # scroll = self._gtk.ScrolledWindow()
        # scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        # scroll.set_kinetic_scrolling(True)
        # scroll.get_overlay_scrolling()
        # scroll.set_hexpand(True)
        # scroll.add(gridBox)
        # scroll.set_min_content_height(self._screen.height / 2)
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        right_box.set_name("printing-right-box")
        right_box.pack_start(rightInfo_box, True, False, 0)
        right_box.pack_start(self.scale_printProgress, False, True, 0)
        right_box.pack_end(self.selectableBox, False, False, 0)
        right_box.set_valign(Gtk.Align.START)
        #right_box.pack_end(scroll, False, False, 0)
        fixed = Gtk.Fixed()
        fixed.set_valign(Gtk.Align.START)
        fixed.set_halign(Gtk.Align.START)
        fixed.put(right_box, 5, 0)
        fixed.put(prevButtonBox, 0, 350)
        fixed.put(nextButtonBox, 540, 350)
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main_box.pack_start(left_box, False, False, 0)
        main_box.pack_start(fixed, False, False, 0)
        main_box.set_valign(Gtk.Align.START)
        pagee = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # pagee.set_hexpand(True)
        # pagee.set_vexpand(True)
        pagee.pack_start(main_box, True, True, 0)      
        pagee.pack_end(BottomMenu(self, False), False, True, 0)
        self.content.add(pagee)

    def generateGrid(self):
        if self.selectableBox.get_children() != None:
            for child in self.selectableBox.get_children():
                self.selectableBox.remove(child)
        if self.startIndex == 1:
            self.selectableBox.pack_start(self.firstPageBox, False, False, 0)
            #self.selectableBox.pack_start(self.separatorFirst, True, False, 0)
            #self.selectableBox.pack_start(self.speedFactor_box, False, False, 0)
        if self.startIndex == 2:
            self.selectableBox.pack_start(self.extrusionFactor_box, False, False, 0)
            #self.selectableBox.pack_start(self.fanSpeed_box, False, False, 0)  
            #self.selectableBox.pack_start(self.fanSpeed_box, False, False, 0)
        #if self.startIndex == 3:
            #self.selectableBox.pack_start(self.extrusionFactor_box, False, False, 0)
            #self.selectableBox.pack_start(self.machine_Box, False, False, 0)
        #if self.startIndex == 4:
           #self.selectableBox.pack_start(self.fanSpeed_box, False, False, 0)    
        self.content.show_all()

    def show_next_page(self, widget):
        self.startIndex = self.startIndex +1
        if self.startIndex > 2:
            self.startIndex = 2
        self.generateGrid()       

    def show_prev_page(self, widget):
        self.startIndex = self.startIndex -1
        if self.startIndex < 1:
            self.startIndex =1
        self.generateGrid()

    def chanceOffset(self,widget,  number):
        self.buttonss[f"{self.OffsetConstant}"].get_style_context().remove_class("change-offset-button-active")
        self.buttonss[f"{number}"].get_style_context().add_class("change-offset-button-active")
        self.OffsetConstant = number

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

    def change_extruder_temperature_pre(self, target):
        max_temp = float(self._printer.get_config_section(self._printer.selectedExtruder)['max_temp'])
        if self.validate(self._printer.selectedExtruder, target, max_temp):
            self.extruder_temp_target = target
            self.change_extruder_temperature(self.extruder_temp_target)

    def change_extruder_temperature(self,temp):
        max_temp = float(self._printer.get_config_section(self._printer.selectedExtruder)['max_temp'])
        if self.validate(self._printer.selectedExtruder, temp, max_temp):
            self._screen._ws.klippy.set_tool_temp(self._printer.get_tool_number(self._printer.selectedExtruder), temp)

    def change_bed_temperature_pre(self, target):
        max_temp = float(self._printer.get_config_section('heater_bed')['max_temp'])
        if self.validate('heater_bed', target, max_temp):
            self.heater_bed_temp_target = target
            self.change_bed_temperature(self.heater_bed_temp_target)

    def change_bed_temperature(self, temp):
        max_temp = float(self._printer.get_config_section('heater_bed')['max_temp'])
        if self.validate('heater_bed', temp, max_temp):
            self._screen._ws.klippy.set_bed_temp(temp)

    def on_button_toggled(self, button, name):
        if button.get_active():
            print(1 + " seçildi")

    def del_obj(self):
        self.isFirst = True
    isFirst = True

    def process_update(self, action, data):
        # if self._printer.state == 'error' or self._printer.state == 'shutdown' or self._printer.state ==  'disconnected':
        #     page_url = 'co_print_home_not_connected_screen'
        #     self._screen.show_panel(page_url, page_url, "Language", 1, False)
        if action == 'notify_status_update' and 'print_stats' in data :
            if 'state'in data['print_stats']:
                if data['print_stats']['state'] == 'paused' :
                    self.enable_button("resume", "cancel")
                    for child in self.button_pause_box.get_children():
                        self.button_pause_box.remove(child)
                    self.button_pause_box.add(self.buttons['resume'])
                    self.buttons['resume'].show()
                elif data['print_stats']['state'] == 'printing':
                    self.enable_button( "pause", "cancel")
                    for child in self.button_pause_box.get_children():
                        self.button_pause_box.remove(child)
                    self.button_pause_box.add(self.buttons['pause'])
                    self.buttons['pause'].show()
        self.ExtruderMax_temp = float(self._printer.get_config_section('extruder')['max_temp'])
        self.HeaterBedMax_temp = float(self._printer.get_config_section('heater_bed')['max_temp'])
        extruder_list = self._printer.get_tools()
        for extruder in extruder_list:
            if self._printer.data[extruder]["motion_queue"] != None:
                if self._printer.selectedExtruder != extruder:
                    self._printer.selectedExtruder = extruder
                    self.extruderChanged = False
                    self.connectedExtruder.set_label(self._printer.selectedExtruder)
        if self._printer.state != 'error' :
            heater_bed_temp = 0
            heater_bed_array = self._printer.get_temp_store('heater_bed')
            if(heater_bed_array):
                heater_bed_temp = heater_bed_array['temperatures'][-1]
                self.heater_bed_temp_target = heater_bed_array['targets'][-1]
            extruder_temp = 0
            extruder_array = self._printer.get_temp_store('extruder')
            if(extruder_array):
                extruder_array = self._printer.get_temp_store('extruder')
                extruder_temp = extruder_array['temperatures'][-1]
                self.extruder_temp_target = extruder_array['targets'][-1]
            if (('toolhead' in self._printer.data) and ('max_velocity' in self._printer.data['toolhead'])):
                machine_velocity = self._printer.data['toolhead']['max_velocity']
                square_corner_velocity = self._printer.data['toolhead']['square_corner_velocity']
                max_accel = self._printer.data['toolhead']['max_accel']
                #max_accel_to_decel = self._printer.data['toolhead']['max_accel_to_decel']
                if(self.velocityInput.getValue() != int(machine_velocity)):
                    self.velocityInput.updateValue(int(machine_velocity))
                if(self.squareCornerInput.getValue() != float(square_corner_velocity)):
                    self.squareCornerInput.updateValue(float(square_corner_velocity))
                if(self.acceleration.getValue() != int(max_accel)):
                    self.acceleration.updateValue(int(max_accel))
                #if(self.maxAcceltoDecel.getValue() != int(max_accel_to_decel)):
                #    self.maxAcceltoDecel.updateValue(int(max_accel_to_decel))
            if self.isFirst:
                self.isFirst = False
                if(self._printer.data['fan'] != {} and self._printer.data['fan']['speed']):
                    if  self.fanSpeed_newValue != self._printer.data['fan']['speed']:
                        self.fanSpeed_newValue = self._printer.data['fan']['speed']
                        self.fanSpeed_widget.updateValue(self.fanSpeed_newValue, str(self.fanSpeed_newValue))
                if(self._printer.data['gcode_move']['speed_factor']):
                    if self.speedFactor_newValue != self._printer.data['gcode_move']['speed_factor'] :
                        self.speedFactor_newValue = self._printer.data['gcode_move']['speed_factor']
                        self.speedFactor_widget.updateValue(self.speedFactor_newValue, str(self.speedFactor_newValue))
                if(self._printer.data['gcode_move']['extrude_factor']):
                    if (self.extrusionFactor_newValue != self._printer.data['gcode_move']['extrude_factor']):
                        self.extrusionFactor_newValue = self._printer.data['gcode_move']['extrude_factor']
                        self.extrusionFactor_widget.updateValue(self.extrusionFactor_newValue, str(self.extrusionFactor_newValue))
                if  action != 'notify_busy' and "gcode_move" in data :
                    if "homing_origin" in data["gcode_move"]:
                        if self.zoffset != float(self._printer.data["gcode_move"]["homing_origin"][2]):
                            logging.info(f"Z Offset: {self.zoffset} -> {float(self._printer.data['gcode_move']['homing_origin'][2])}")
                            self.zoffset = float(self._printer.data["gcode_move"]["homing_origin"][2])
                            self.zoffset_widget.updateValue(self.zoffset)

                data = self._printer.data
                if self.speed_factor*100 != data['gcode_move']['speed_factor']:
                    self.speed_factor = data['gcode_move']['speed_factor']
                    self.speedFactor_widget.updateValue(self.speed_factor*100, str(int(self.speed_factor*100)))
                if self.extrude_factor*100 != data['gcode_move']['extrude_factor']:
                    self.extrude_factor = data['gcode_move']['extrude_factor']
                    self.extrusionFactor_widget.updateValue(self.extrude_factor*100, str(int(self.extrude_factor*100)))
                if self._printer.data['fan'] != {} and self.fan_spped*100 != data['fan']['speed']:
                    self.fan_spped = data['fan']['speed'] 
                    self.fanSpeed_widget.updateValue(self.fan_spped*100, str(int(self.fan_spped*100)))
                if self.zoffset != float(self._printer.data["gcode_move"]["homing_origin"][2]):
                    logging.info(f"Z Offset: {self.zoffset} -> {float(self._printer.data['gcode_move']['homing_origin'][2])}")
                    self.zoffset = float(self._printer.data["gcode_move"]["homing_origin"][2])
                    self.zoffset_widget.updateValue(self.zoffset)
                if self.pressure_advance != float(self._printer.data["extruder"]["pressure_advance"]):
                    self.pressure_advance = float(self._printer.data["extruder"]["pressure_advance"])
                    self.pressureAdvanceInput.updateValue(self.pressure_advance)
                if self.smooth_time != float(self._printer.data["extruder"]["smooth_time"]):
                    self.smooth_time = float(self._printer.data["extruder"]["smooth_time"])
                    self.smoothTimeInput.updateValue(self.smooth_time)
            if(self.extruder_temp_target != 0):
                    self.extruder.updateValue(extruder_temp/self.extruder_temp_target, str(round(extruder_temp,1)) + f"° / {self.extruder_temp_target}°")
            else:
                    self.extruder.updateValue(1/1, str(round(extruder_temp,1)) + f"° / {self.extruder_temp_target}°")
            if(self.heater_bed_temp_target != 0):
                    self.heatedBed.updateValue(heater_bed_temp/self.heater_bed_temp_target, str(round(heater_bed_temp,1)) + f"° / {self.heater_bed_temp_target}°")
            else:
                    self.heatedBed.updateValue(1/1, str(round(heater_bed_temp,1)) + f"° / {self.heater_bed_temp_target}°")
            ps = self._printer.get_stat("print_stats")
            if 'filename' in ps and (ps['filename'] != self.filename):
                logging.debug(f"Changing filename: '{self.filename}' to '{ps['filename']}'")
                self.image_load(ps['filename'])
                self.filename = ps['filename']
                self.labels['file'].set_text('Printing File: ' + self._screen.rename_string_printer(self.filename,15))
            if 'print_duration' in ps:
                total_duration = ps['total_duration']
                print_duration = ps['print_duration']
                self.update_time_left(total_duration, print_duration, ps['filament_used'])

    def image_load(self, filepath):
        self.pixbuf = self.get_file_image(filepath, self._screen.width / 3, self._screen.height / 3,small=False)
        if self.pixbuf is not None:
            self.labels['thumbnail'].set_from_pixbuf(self.pixbuf)
            #self.labels['files'][filepath]['icon'].set_image(Gtk.Image.new_from_pixbuf(pixbuf))
       
    def update_time_left(self, total_duration, print_duration, fila_used=0):
        self.update_file_metadata()
        non_printing = total_duration - print_duration
        estimated = None
        slicer_time = filament_time = file_time = None
        timeleft_type = self._config.get_config()['main'].get('print_estimate_method', 'auto')
        self.progress = 1
        if "gcode_start_byte" in self.file_metadata:
            self.progress = (max(self._printer.get_stat('virtual_sdcard', 'file_position') -
                            self.file_metadata['gcode_start_byte'], 0) / (self.file_metadata['gcode_end_byte'] -
                                                                          self.file_metadata['gcode_start_byte']))
        else:
            self.progress = self._printer.get_stat('virtual_sdcard', 'progress')
        with contextlib.suppress(Exception):
            if self.file_metadata['filament_total'] > fila_used:
                filament_time = (total_duration / (fila_used / self.file_metadata['filament_total'])) + non_printing
        with contextlib.suppress(ZeroDivisionError):
            file_time = (total_duration / self.progress) + non_printing
        with contextlib.suppress(KeyError):
            if self.file_metadata['estimated_time'] > 0:
                usrcomp = (self._config.get_config()['main'].getint('print_estimate_compensation', 100) / 100)
                spdcomp = sqrt(self.speed_factor)
                slicer_time = ((self.file_metadata['estimated_time'] * usrcomp) / spdcomp) + non_printing
        if timeleft_type == "file":
            estimated = file_time
        elif timeleft_type == "filament":
            estimated = filament_time
        elif slicer_time is not None:
            if timeleft_type == "slicer":
                estimated = slicer_time
            elif filament_time is not None and self.progress > 0.14:
                # Weighted arithmetic mean (Slicer is the most accurate)
                estimated = (slicer_time * 3 + filament_time + file_time) / 5
            else:
                # At the begining file and filament are innacurate
                estimated = slicer_time
        elif file_time is not None:
            if filament_time is not None:
                estimated = (filament_time + file_time) / 2
            else:
                estimated = file_time - non_printing
        if estimated is not None:
            progressValue=    1-((estimated - total_duration)/estimated)
            remaining =   self.format_eta(estimated, total_duration)   
        else:
            progressValue = 0
            remaining =   '-'   
        if self._printer.state == "ready":
            remaining = '-'
            progressValue= 1
        self.scale_printProgress.set_fraction(progressValue)
        self.labels['status'].set_label(("Estimated Time") + ": " + remaining)

    def update_file_metadata(self):
        if self._files.file_metadata_exists(self.filename):
            self.file_metadata = self._files.get_file_info(self.filename)
            #logging.info(f"Update Metadata. File: {self.filename} Size: {self.file_metadata['size']}")
            #self.show_file_thumbnail()
            if "object_height" in self.file_metadata:
                self.oheight = float(self.file_metadata['object_height'])
                if "layer_height" in self.file_metadata:
                    self.layer_h = float(self.file_metadata['layer_height'])
                    if "first_layer_height" in self.file_metadata:
                        self.f_layer_h = float(self.file_metadata['first_layer_height'])
                    else:
                        self.f_layer_h = self.layer_h
        else:
            self.file_metadata = {}
            #logging.debug("Cannot find file metadata. Listening for updated metadata")
            self._screen.files.add_file_callback(self._callback_metadata)

    def has_thumbnail(self, filename):
        if filename not in self.files:
            return False
        return "thumbnails" in self.files[filename] and len(self.files[filename]) > 0
    
    def show_file_thumbnail(self):
        if self.has_thumbnail(self.filename):
            if self._screen.vertical_mode:
                width = self._screen.width * 0.9
                height = self._screen.height / 4
            else:
                width = self._screen.width / 3
                height = self._gtk.content_height * 0.47
           

    def _callback_metadata(self, newfiles, deletedfiles, modifiedfiles):
        if not bool(self.file_metadata) and self.filename in modifiedfiles:
            self.update_file_metadata()
            self._files.remove_file_callback(self._callback_metadata)

    
    def set_fan_speed(self, progressType, value):
        if progressType == "fan":
            self._screen._ws.klippy.gcode_script(KlippyGcodes.set_fan_speed(value))
        elif progressType == "extrusionFactor":
            self._screen._ws.klippy.gcode_script(KlippyGcodes.set_extrusion_rate(value))
        elif progressType =="speedFactor":
            self._screen._ws.klippy.gcode_script(KlippyGcodes.set_speed_rate(value))

    def check_fan_speed(self, fan):
        #self.update_fan_speed(None, fan, self._printer.get_fan_speed(fan))
        return False
    
    def cancelPrint(self, widget):
        print('cancel')
        buttons = [
            {"name": _("Cancel Print"), "response": Gtk.ResponseType.APPLY},
            {"name": _("Go Back"), "response": Gtk.ResponseType.CANCEL}
        ]
        if len(self._printer.get_stat("exclude_object", "objects")) > 1:
            buttons.insert(0, {"name": _("Exclude Object"), "response": Gtk.ResponseType.APPLY})
        label = Gtk.Label()
        label.set_markup(_("Are you sure you wish to cancel this print?"))
        label.set_hexpand(True)
        label.set_halign(Gtk.Align.CENTER)
        label.set_vexpand(True)
        label.set_valign(Gtk.Align.CENTER)
        label.set_line_wrap(True)
        label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        dialog = self._gtk.Dialog(self._screen, buttons, label, self.cancel_confirm)
        dialog.set_title(_("Cancel"))

    def cancel_confirm(self, dialog, response_id):
        self._gtk.remove_dialog(dialog)
        if response_id == Gtk.ResponseType.APPLY:
            # self.objects = self._printer.get_stat("exclude_object", "objects")
            # self.labels['map'] = None
            # #self._screen._ws.klippy.emergency_stop()
            # #self._screen._ws.klippy.restart_firmware()
            # #for obj in self.objects:
            # name = self.filename
            # logging.info(f"Adding {name}")
            # script = {"script": f"EXCLUDE_OBJECT NAME={'Servo_holder_fus_X.gcode'}"}
            # self._screen._confirm_send_action(
            # dialog,
            # _("Are you sure do you want to exclude the object?") + f"\n\n{name}",
            # "printer.gcode.script",
            # script
            # )
            self._screen._ws.klippy.print_cancel(self._response_callback)
            return
        if response_id == Gtk.ResponseType.CANCEL:
            self.enable_button("pause", "cancel")
            return
        logging.debug("Canceling print")
        self.filename = ""
        self.disable_button("pause", "resume", "cancel")
        self._screen._ws.klippy.print_cancel(self._response_callback)
    
    def disable_button(self, *args):
        for arg in args:
            self.buttons[arg].set_sensitive(False)

    def pausePrint(self, widget):       
        self._screen._ws.klippy.print_pause(self._response_callback, "enable_button", "resume", "cancel")
        for child in self.button_pause_box.get_children():
            self.button_pause_box.remove(child)
        self.button_pause_box.add(self.buttons['resume'])
        #self.button_pause_box.show()
        self.buttons['resume'].show()
        print('pause')
        #self.content.show_all()  
        return True

    def resumePrint(self, widget):
        self._screen._ws.klippy.print_resume(self._response_callback, "enable_button", "pause", "cancel")
        for child in self.button_pause_box.get_children():
            self.button_pause_box.remove(child)
        self.button_pause_box.add(self.buttons['pause'])
        self.buttons['pause'].show()
        print('pause')
        return True
        #self._screen.show_all()

    def _response_callback(self, response, method, params, func=None, *args):
        if func == "enable_button":
            self.enable_button(*args)

    def enable_button(self, *args):
        for arg in args:
            self.buttons[arg].set_sensitive(True)
            
    def create_buttons(self):
        self.buttons = {
            'cancel': self._gtk.Button("close_print", None, "close", .5),
            'pause': self._gtk.Button("pause_print", None, "pause", .5),
            'resume': self._gtk.Button("resume", None, "resume", .5),
        }
        # self.labels['graph_settemp'].connect("clicked", self.show_numpad)
        self.buttons['cancel'].connect("clicked", self.cancelPrint)
        self.buttons['pause'].connect("clicked", self.pausePrint)
        self.buttons['resume'].connect("clicked", self.resumePrint)
        
    def cancel(self, widget):
        buttons = [
            {"name": _("Cancel Print"), "response": Gtk.ResponseType.OK},
            {"name": _("Go Back"), "response": Gtk.ResponseType.CANCEL}
        ]
        if len(self._printer.get_stat("exclude_object", "objects")) > 1:
            buttons.insert(0, {"name": _("Exclude Object"), "response": Gtk.ResponseType.APPLY})
        label = Gtk.Label()
        label.set_markup(_("Are you sure you wish to cancel this print?"))
        label.set_hexpand(True)
        label.set_halign(Gtk.Align.CENTER)
        label.set_vexpand(True)
        label.set_valign(Gtk.Align.CENTER)
        label.set_line_wrap(True)
        label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        
    def show_numpad(self, widget, device=None):
        dialog = KeyPadNew(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        dialog.destroy()

    def change_target_temp(self, temp):
        return True
    
    def hide_numpad(self, widget=None):
        self.devices[self.active_heater]['name'].get_style_context().remove_class("button_active")
        self.active_heater = None

        for d in self.active_heaters:
            self.devices[d]['name'].get_style_context().add_class("button_active")

        if self._screen.vertical_mode:
            self.grid.remove_row(1)
            self.grid.attach(self.create_right_panel(), 0, 1, 1, 1)
        else:
            self.grid.remove_column(1)
            self.grid.attach(self.create_right_panel(), 1, 0, 1, 1)
        self.grid.show_all()