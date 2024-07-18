import datetime
import logging
import os
import time
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.hometab import HomeTab
from ks_includes.widgets.infodialog import InfoDialog
from ks_includes.widgets.keypad import Keypad
from ks_includes.widgets.progressbar import ProgressBar
from ks_includes.widgets.mainbutton import MainButton
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf
from ks_includes.screen_panel import ScreenPanel
from datetime import datetime, timedelta

# def create_panel(*args):
#     return CoPrintHomeScreen(*args)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# class CoPrintHomeScreen(ScreenPanel, metaclass=Singleton):
class Panel(ScreenPanel, metaclass=Singleton):
    total_jobs = -1
    instant_cpu = 0
    instant_mem = 0
    active_heater = None
    extruderChanged = False
    getToolsActivated = False
    desiredTemp = 1
    temp_extruder_temp = 0
    temp_heater_bed_temp = 0
    print_stats = []
    total_used = {}
    mcu_version = ''
    filament_usage_array = []
    mcu_constants = None
    mcus = []
    hostInfo = None
    
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.extruders = self._printer.extruders
        self.current_time_millis = int(round(time.time() * 1000))
        self.extruder_temp_target = 0
        self.heater_bed_temp_target = 0
        self.extruder_temp_target_pre = 0
        self.heater_bed_temp_target_pre= 0
        self.h = 1
        grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=15,
                         row_spacing=15)
        row = 0
        count = 0
        extruderIndex = 0

        for extruder in self.extruders:

            extruder['Image'] = self._gtk.Image(extruder['Icon'], self._gtk.content_width * .11 , self._gtk.content_height * .11)
            extruder['RadioButton'] = self._gtk.Image('passive', self._gtk.content_width * .05 , self._gtk.content_height * .05)

            alignment = Gtk.Alignment.new(1, 0, 0, 0)
            alignment.add(extruder['RadioButton'])

            extruderBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            extruderBox.set_name("home-extruder-select-box-home")
            extruderBox.pack_start(alignment, False, False, 5)
            extruderBox.pack_start(extruder['Image'], False, True, 5)

            eventBox = Gtk.EventBox()

            eventBox.add(extruderBox)
            extruder['EventBox'] = Gtk.Frame(name= "extrude")
            extruder['EventBox'].add(eventBox)
            grid.attach(extruder['EventBox'], count, row, 1, 1)
            count += 1
            extruderIndex +=1
            if count % 4 == 0:
                count = 0
                row += 1


        self.preheat_options = self._screen._config.get_preheat_options()

        menu = BottomMenu(self, False)

        extruderBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing= 0)
        extruderBox.set_name("extruder-box")
        self.extruder = ProgressBar(self, "0.0° / 0.0°", "extrudericon", 0.5, "progress-bar-extruder-blue", self.change_extruder_temperature_pre)
        extruderBox.pack_start(self.extruder, True, True, 0)
        self.extruderSwitch = Gtk.Switch(name = "extruder-switch")
        self.extruderSwitch.connect("notify::active", self.on_switch_activated, 'extruder')
        extruderBox.pack_start(self.extruderSwitch, False, False, 0)


        PLAButton = Gtk.Button(_("Preheat PLA"),name ="pla-abs-button")
        PLAButton.connect("clicked", self.set_temperature,  'PLA')
        PLAButton.set_hexpand(True)


        extruderWithButton_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing= 0)
        extruderWithButton_box.pack_start(extruderBox, False, True, 0)
        extruderWithButton_box.pack_start(PLAButton, True, True, 0)
        extruderWithButton_box.set_valign(Gtk.Align.CENTER)

        labelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        labelBox.set_valign(Gtk.Align.CENTER)
        labelBox.set_name("move-label-box")

        connectedExtruderLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        connectedExtruderLabelBox.set_name("extruder-heatedbad-label-box")
        connectedExtruderLabelBox.set_valign(Gtk.Align.CENTER)
        self.connectedExtruder = Gtk.Label("Extruder Temperature", name="connected-extruder-label")
        self.connectedExtruder.set_justify(Gtk.Justification.LEFT)
        connectedExtruderLabelBox.pack_start(self.connectedExtruder, False, False, 0)
        connectedExtruderBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        connectedExtruderBox.pack_start(connectedExtruderLabelBox, False, False, 0)
        connectedExtruderBox.pack_start(extruderWithButton_box, False, False, 0)


        heatedBedBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing= 0)
        heatedBedBox.set_name("extruder-box")
        self.heatedBed = ProgressBar(self, "0.0° / 0.0°", "tablaicon", 0.5, "progress-bar-extruder-yellow", self.change_bed_temperature_pre)
        heatedBedBox.pack_start(self.heatedBed, True, True, 0)
        self.heatedBedSwitch = Gtk.Switch(name = "extruder-switch")
        self.heatedBedSwitch.connect("notify::active", self.on_switch_activated, 'heater_bed')

        heatedBedBox.pack_start(self.heatedBedSwitch, False, False, 0)

        ABSButton = Gtk.Button(_("Preheat ABS"),name ="pla-abs-button")
        ABSButton.connect("clicked", self.set_temperature,  'ABS')

        ABSButton.set_hexpand(True)

        heatedBedWithButton_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing= 0)
        heatedBedWithButton_box.pack_start(heatedBedBox, False, True, 0)
        heatedBedWithButton_box.pack_start(ABSButton, True, True, 0)

        connectedHeatedBedLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        connectedHeatedBedLabelBox.set_name("extruder-heatedbad-label-box")
        connectedHeatedBedLabelBox.set_valign(Gtk.Align.CENTER)
        connectedHeated = Gtk.Label(_("Heated Bed"), name="connected-extruder-label")
        connectedHeated.set_justify(Gtk.Justification.LEFT)
        connectedHeatedBedLabelBox.pack_start(connectedHeated, False, False, 0)
        connectedHeatedBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        connectedHeatedBox.pack_start(connectedHeatedBedLabelBox, False, False, 0)
        connectedHeatedBox.pack_start(heatedBedWithButton_box, False, False, 0)

        ###########################
        
        self.tab_box = HomeTab(self)
      
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        left_box.pack_start(connectedExtruderBox, False, False, 0)
        left_box.pack_start(connectedHeatedBox, False, False, 0)

        left_box.pack_start(self.tab_box, False, False, 0)

        homeButton = MainButton(self, "home", _("Homing"), "home-home", "co_print_home_screen", 1.2, True)
        moveButton = MainButton(self, "move", _("Move Axis"), "home-move", 'co_print_move_axis_screen', 1.2, False)
        startButton = MainButton(self, "baskibaslat", _("Start Print"), "home-start", "co_print_printing_screen", 1.2, False)
        settingButton = MainButton(self, "ayarlar", _("Settings"), "home-setting", "co_print_setting_screen", 1.2, False)
        extrudeButton = MainButton(self, "extrudericon", _("Extrude"), "home-extrude", "co_print_extruders_screen", 1.2, False)
        temperatureButton = MainButton(self, "sicaklik", _("Temperature"), "home-temperature", "co_print_temperature_screen", 1.2, False)

        menuGrid = Gtk.Grid()
        menuGrid.set_column_spacing(10)
        menuGrid.set_row_spacing(10)
        menuGrid.set_column_homogeneous(True)
        menuGrid.attach(homeButton, 0, 0, 1, 1)
        menuGrid.attach(moveButton, 1, 0, 1, 1)
        menuGrid.attach(startButton, 0, 1, 1, 1)
        menuGrid.attach(settingButton, 1, 1, 1, 1)
        menuGrid.attach(extrudeButton, 0, 2, 1, 1)
        menuGrid.attach(temperatureButton, 1, 2, 1, 1)

        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        right_box.pack_start(menuGrid, True, True, 0)

        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main_box.pack_start(left_box, True, False, 0)
        main_box.pack_start(right_box, True, False, 0)
        main_box.set_vexpand(True)
        #main_box.set_valign(Gtk.Align.CENTER)
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(main_box, True, True, 0)
        page.pack_end(menu, False, True, 0)

        self._screen._ws.send_method("server.history.totals", None, self.finished_history)
        self._screen._ws.send_method("printer.info", None, self.finished_printer_info)
        self._screen._ws.send_method("server.files.get_directory", None, self.finished_server_get_directory)
        self._screen._ws.send_method("printer.objects.subscribe", {"objects":{"webhooks":None,"configfile":None,"mcu":None,"gcode_move":None,"print_stats":None,"virtual_sdcard":None,"heaters":None,"heater_bed":None,"fan":None,"gcode_macro LOAD_FILAMENT":None,"gcode_macro UNLOAD_FILAMENT":None,"gcode_macro START_PRINT_PLA":None,"gcode_macro go_screw_1":None,"gcode_macro go_screw_2":None,"gcode_macro go_screw_3":None,"gcode_macro go_screw_4":None,"stepper_enable":None,"motion_report":None,"query_endstops":None,"idle_timeout":None,"system_stats":None,"manual_probe":None,"toolhead":None,"extruder":None}}, self.finished_printer_mcus)

        self.content.add(page)





    def get_filament_usage_array(self, state):
        output = []
        start_date = datetime.now() - timedelta(days=6)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        jobs_filtered = [
            job for job in state['jobs'] if datetime.utcfromtimestamp(job['start_time']) >= start_date and job['filament_used'] > 0
        ]

       

        for i in range(7):
            tmp_date = start_date + timedelta(days=i)
            output.append([int(tmp_date.timestamp()), 0])

        if jobs_filtered:
            for current in jobs_filtered:
                current_start_date = datetime.utcfromtimestamp(current['start_time']).replace(hour=0, minute=0, second=0, microsecond=0)
                index = next((i for i, element in enumerate(output) if element[0] == int(current_start_date.timestamp())), -1)
                if index != -1:
                    output[index][1] += round(current['filament_used'] / 1000, 2)

        return sorted(output, key=lambda x: x[0], reverse=True)

    def finished_printer_mcus(self, result, method, params):
         #print(result)
         self.mcu_constants = result['result']['status']
     
    def finished_printer_info(self, result, method, params):
        self.printer_version = result['result']['software_version']
        self._screen._ws.send_method("machine.system_info", None, self.finished_system_info)
        #print(result['result']['software_version'])

    def finished_server_get_directory(self, result, method, params):
        if 'software_version' in result['result']:
            print(result['result']['software_version'])

   

    def format_filesize(self, file_size_in_bytes):
        i = -1
        byte_units = [' kB', ' MB', ' GB', ' TB', ' PB', ' EB', ' ZB', ' YB']
        while file_size_in_bytes > 1024:
            file_size_in_bytes /= 1024
            i += 1

        return f"{max(file_size_in_bytes, 0.1):.1f}{byte_units[i]}"

    def finished_system_info(self, result, method, params):
        state = result['result']
        #print(state)
        class HostStats:
            def __init__(self):
                self.cpuName = None
                self.cpuDesc = None
                self.bits = None
                self.version = None
                self.pythonVersion = None
                self.os = None
                self.release_info = None
                self.load = 0
                self.loadPercent = 0
                self.loadProgressColor = 'primary'
                self.memoryFormat = None
                self.memUsed = '0 B'
                self.memAvail = '0 B'
                self.memTotal = '0 B'
                self.memUsage = None
                self.memUsageColor = 'primary'
                self.tempSensor = {'temperature': 0, 'measured_min_temp': None, 'measured_max_temp': None}
        output = HostStats()
        if 'system_info' in state:
            version = None
            if  self.printer_version:
                version = '-'.join(self.printer_version.split('-')[:4])
            python_version = None
            if state['system_info'].get('python') and state['system_info']['python'].get('version_string'):
                first_space = state['system_info']['python']['version_string'].find(' ')
                python_version = state['system_info']['python']['version_string'][:first_space + 1]
            cpu_cores = state['system_info']['cpu_info']['cpu_count'] if state['system_info']['cpu_info'].get('cpu_count') else 1
            #load = round((root_state.get('printer', {}).get('system_stats', {}).get('sysload', 0)) * 100) / 100
            load = 0
            load_percent = round((load / cpu_cores) * 100)
            output.loadProgressColor = 'primary'
            if load_percent > 95:
                output.loadProgressColor = 'error'
            elif load_percent > 80:
                output.loadProgressColor = 'warning'
            memory_format = None
            mem_usage = None
            mem_avail = self.usage_info['system_memory']['available'] * 1024
            mem_total =  self.usage_info['system_memory']['total'] * 1024
            if mem_avail > 0 and mem_total > 0:
                memory_format = f"{self.format_filesize(mem_total - mem_avail)} / {self.format_filesize(mem_total)}"
                mem_usage = round(((mem_total - mem_avail) / mem_total) * 100)
            elif mem_total:
                memory_format = self.format_filesize(mem_total)
            mem_usage_color = 'primary'
            if mem_usage and mem_usage > 95:
                mem_usage_color = 'error'
            elif mem_usage and mem_usage > 80:
                mem_usage_color = 'warning'
            output.cpuName = state['system_info']['cpu_info'].get('processor', None)
            output.cpuDesc = state['system_info']['cpu_info'].get('cpu_desc', None)
            output.bits = state['system_info']['cpu_info'].get('bits', None)
            output.version = version
            output.pythonVersion = python_version
            output.os = state['system_info']['distribution'].get('name', None)
            output.release_info = state['system_info']['distribution'].get('release_info', None)
            output.load = load
            output.loadPercent = min(load_percent, 100)
            output.memoryFormat = memory_format
            output.memUsed = self.format_filesize(mem_total - mem_avail)
            output.memAvail = self.format_filesize(mem_avail)
            output.memTotal = self.format_filesize(mem_total)
            output.memUsage = mem_usage
            output.memUsageColor = mem_usage_color
          
            self.hostInfo = output


    def finished_history_list(self, result, method, params):
        arr2 = {}
        print(result)
        self.filament_usage_array = self.get_filament_usage_array(result['result'])
        for d in result['result']['jobs']:
            t = arr2.setdefault(d['status'], [])
            t.append(d)
        self.print_stats = []   
        keysList = list(arr2.keys())    
        for key in keysList:
            print(key + ': ' + str(len(arr2[key])))
            print_stat = {'name': key, 'value': len(arr2[key])}
            self.print_stats.append(print_stat)
        self.tab_box.static_value()

    def finished_history(self, result, method, params):
        if result['result']['job_totals']['total_jobs'] == self.total_jobs:
            self.tab_box.static_value()
        else:
            self.total_jobs = result['result']['job_totals']['total_jobs']
            self.total_used = {'total_filament_used': result['result']['job_totals']['total_filament_used'],
                               'total_print_time': result['result']['job_totals']['total_print_time'],
                               'total_time': result['result']['job_totals']['total_time'],
                               'total_jobs': result['result']['job_totals']['total_jobs']}
            self._screen._ws.send_method("server.history.list", None, self.finished_history_list)

    def on_switch_activated(self, switch, gparam,switchName):
        temp = 0
        if switch.get_active():
            if(switchName == 'extruder'):
                if self.extruder_temp_target_pre != 0:
                    temp = self.extruder_temp_target_pre
                else:
                    temp = 200
            else:
                if self.heater_bed_temp_target_pre != 0:
                    temp = self.heater_bed_temp_target_pre
                else:
                    temp = 60 
        else:
            if(switchName == 'extruder'):
                self.extruder_temp_target_pre = temp
            else:
                self.heater_bed_temp_target_pre = temp

        if(switchName == 'extruder'):
            self.change_extruder_temperature(temp)
        else:
            self.change_bed_temperature(temp)


    def chanceExtruder(self, eventBox, gparam, extruder):
        for i, item in enumerate(self.extruders):
            if item['Extrude'] != extruder:
                item['EventBox'].get_style_context().remove_class("filament-extruder-active")
            else:
                self._printer.selectedExtruder = extruder
                item['EventBox'].get_style_context().add_class("filament-extruder-active")
                self._screen._ws.klippy.gcode_script("T" + str(i))

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
        
        self.timeout_id = GLib.timeout_add(1000, self.on_timeout, None)
       

    
    def on_timeout(self, *args, **kwargs):
        self.desiredTemp = 1
        self.timeout_id = None
        #self.destroy()
        return False


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

    def filament_cut(self, widget):
        self._screen._ws.klippy.gcode_script(
            "FILAMENT_CUT"  # FILAMENT_CUT
        )

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
                if setting == "cooldown" :
                    if target is None and target != 0 and not heater.startswith('temperature_fan ') :
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
        logging.info(f"Showing numpad for")
        self.grid.show_all()
        self.labels['popover'].popdown()

    def __del__(self):
        self.desiredTemp = 1
        print('Destructor called, Employee deleted.')

    def del_obj(self):
        self.desiredTemp = 1
        self.extruderChanged = False

    def format_frequency(self, frequency):
        i = -1
        units = [' kHz', ' MHz', ' GHz']
        while frequency > 1000:
            frequency /= 1000
            i += 1
        return f"{max(frequency, 0.1):.0f}{units[i]}"
    count = 0
    def process_update(self, action, data):
        if action == 'notify_proc_stat_update':
            self.usage_info = data
            self.count +=1
            self.instant_cpu = data['system_cpu_usage']['cpu']
            self.instant_mem = (data['system_memory']['used']/ data['system_memory']['total'])*100
            if self.count == 4:
                self.count=0
                self.tab_box.updateCPU(self.instant_cpu)
                self.tab_box.updateMEM(self.instant_mem)

        if action == 'notify_status_update':
            for key in data:
                if (key == 'mcu' or key.startswith('mcu ') )and self.mcu_constants != None:
                    self.mcus = []
                    mcu = data[key]
                    version_output = (self.mcu_constants[key].get('mcu_version', 'unknown')).split('-')[:4]
                    version_output = '-'.join(version_output)

                    load = 0
                    if mcu.get('last_stats') and mcu['last_stats'].get('mcu_task_avg') and mcu['last_stats'].get('mcu_task_stddev'):
                        load = mcu['last_stats']['mcu_task_avg'] + (3 * mcu['last_stats']['mcu_task_stddev']) / 0.0025

                    load_progress_color = 'primary'
                    if load > 0.95:
                        load_progress_color = 'error'
                    elif load > 0.8:
                        load_progress_color = 'warning'
                   
                    self.mcus.append({
                        'name': key,
                        'mcu_constants': self.mcu_constants[key]['mcu_constants'],
                        'last_stats': self.mcu_constants[key]['last_stats'],
                        'version': version_output,
                        'chip': self.mcu_constants[key]['mcu_constants']['MCU'] if self.mcu_constants[key]['mcu_constants'] else None,
                        'freq': mcu['last_stats']['freq'] if mcu['last_stats'].get('freq') else None,
                        'freqFormat': self.format_frequency(mcu['last_stats']['freq']) if mcu['last_stats'].get('freq') else None,
                        'awake': "{:.2f}".format(mcu['last_stats']['mcu_awake'] / 5) if mcu['last_stats'].get('mcu_awake') else None,
                        'load': "{:.2f}".format(load),
                        'loadPercent': round(load * 100) if load < 1 else 100,
                        'loadProgressColor': load_progress_color,
                        #'tempSensor': getters.get_mcu_temp_sensor(key),
                    })
                elif(key=='extruder'):
                    if 'target' in data[key]:
                        self.change_extruder_temperature_pre(int(data[key]['target']))
                elif(key == 'heater_bed'):
                    if 'target' in data[key]:
                        self.change_bed_temperature_pre(int(data[key]['target']))
                    

        if self._printer.state != 'error' :

            if len(self._printer.get_tools()) > 0  and self.getToolsActivated == False:
                for d in (self._printer.get_tools() + self._printer.get_heaters()):
                    self.add_device(d)
                i = 0
                self.getToolsActivated = True
                state = self._printer.state
                selection = []

                if state not in ["printing", "paused"]:
                    for extruder in self._printer.get_tools():
                        selection.append(extruder)
                    self.show_preheat = True
                    selection.extend(self._printer.get_heaters())
                else:
                    current_extruder = self._printer.get_stat("toolhead", "extruder")
                    if current_extruder:
                        selection.append(current_extruder)

                # Select heaters
                for h in selection:
                    if h.startswith("temperature_sensor "):
                        continue
                    name = h.split()[1] if len(h.split()) > 1 else h
                    # Support for hiding devices by name
                    if name.startswith("_"):
                        continue
                    if h not in self.active_heaters:
                        self.select_heater(None, h)

            extruder_list = self._printer.get_tools()
            for extruder in extruder_list:
                if self._printer.data[extruder]["motion_queue"] != None:
                    if action == "notify_gcode_response" and data.startswith("// ") and data.endswith("'extruder'"):
                        new_extruder = 'extruder_stepper ' + (data.split()[2].strip("'"))
                        if self._printer.selectedExtruder != new_extruder:
                            self._printer.selectedExtruder = new_extruder
                            self.extruderChanged = False
                        #self.connectedExtruder.set_label(self.selectedExtruder)



            extrude = self._printer.get_config_section('extruder')
            if(extrude):
                self.ExtruderMax_temp = float(extrude['max_temp'])

            if(self.extruderChanged == False):
                self.extruderChanged = True
                i= 0
                for d in (self._printer.get_tools() + self._printer.get_heaters()):
                    self.add_device(d)
                for extruder in self._printer.get_tools():
                    if extruder != 'extruder':
                        self.extruders[i]['RadioButtonStatus'] = True
                        if self.extruders[i]['Extrude'] is None:
                            self.extruders[i]['EventBox'].connect("button-press-event", self.chanceExtruder, extruder)
                        self.extruders[i]['Extrude'] = extruder
                        if self.extruders[i]['Extrude'] != self._printer.selectedExtruder:
                            self.extruders[i]['EventBox'].get_style_context().remove_class("filament-extruder-active")

                        else:
                            self.extruders[i]['EventBox'].get_style_context().add_class("filament-extruder-active")
                        i += 1

                for x in range(i, 8):
                    svg_file = "styles/z-bolt/images/passive.svg"
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(svg_file, self._gtk.content_width * .05,
                                                                    self._gtk.content_height * .05)

                    self.extruders[x]['RadioButton'].set_from_pixbuf(pixbuf)
                    self.extruders[x]['EventBox'].get_style_context().remove_class("extrude-active")
            heater_bed_temp = 0
            heater_bed_array = self._printer.get_temp_store('heater_bed')

            if(heater_bed_array):
                heater_bed_temp = heater_bed_array['temperatures'][-1]
                self.heater_bed_temp_target = heater_bed_array['targets'][-1]

                if(self.heater_bed_temp_target >0 ):

                    #if(self.heatedBedSwitch.get_active()== False ):
                        if self.desiredTemp != 0:
                            self.heater_bed_temp_target_pre = self.heater_bed_temp_target
                            self.heatedBedSwitch.set_active(True)

                else:
                    if(self.heatedBedSwitch.get_active()):
                         if self.desiredTemp != 0:
                            self.heater_bed_temp_target_pre = self.heater_bed_temp_target
                            self.heatedBedSwitch.set_active(False)


            else:
                heater_bed_temp = -1
                #self.heatedBedSwitch.set_active(False)


            extruder_temp = 0
            extruder_array = self._printer.get_temp_store(self._printer.data["toolhead"]["extruder"])

            if(extruder_array):
                extruder_temp = extruder_array['temperatures'][-1]

                self.extruder_temp_target = extruder_array['targets'][-1]

                if(self.extruder_temp_target >0 ):

                    #if(self.extruderSwitch.get_active() == False ):
                        if  self.desiredTemp != 0:
                            self.extruder_temp_target_pre = self.extruder_temp_target
                            self.extruderSwitch.set_active(True)

                else:
                    if(self.extruderSwitch.get_active()):
                         if self.desiredTemp != 0:
                            self.extruder_temp_target_pre = self.extruder_temp_target
                            self.extruderSwitch.set_active(False)
                self.desiredTemp = 0
            else:
                extruder_temp = -1
                #self.extruderSwitch.set_active(False)


            if(self.temp_extruder_temp != extruder_temp):
                self.temp_extruder_temp = extruder_temp
                if(self.extruder_temp_target_pre != 0):
                     self.extruder.updateValue(extruder_temp/self.extruder_temp_target_pre, str(round(extruder_temp,1)) + f"° / {self.extruder_temp_target_pre}°")
                     self.tab_box.updateValue(str(round(extruder_temp,1)) + f"° / {self.extruder_temp_target_pre}°")
                else:
                     self.extruder.updateValue(1/1, str(round(extruder_temp,1)) + f"° / {self.extruder_temp_target_pre}°")
                     self.tab_box.updateValue(str(round(extruder_temp,1)) + f"° / {self.extruder_temp_target_pre}°")

            if(self.temp_heater_bed_temp != heater_bed_temp):
                self.temp_heater_bed_temp = heater_bed_temp
                if(self.heater_bed_temp_target_pre != 0):
                    self.heatedBed.updateValue(heater_bed_temp/self.heater_bed_temp_target_pre, str(round(heater_bed_temp,1)) + f"° / {self.heater_bed_temp_target_pre}°")
                else:
                    self.heatedBed.updateValue(1/1, str(round(heater_bed_temp,1)) + f"° / {self.heater_bed_temp_target_pre}°")

