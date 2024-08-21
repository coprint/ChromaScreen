import contextlib
import logging
import os
from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.keypad_new import KeyPadNew
import gi
from ks_includes.widgets.keypad import Keypad

from ks_includes.widgets.printfile import PrintFile
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintTemperatureScreen(*args)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# class CoPrintTemperatureScreen(ScreenPanel, metaclass=Singleton):
class Panel(ScreenPanel, metaclass=Singleton):

    active_heater = None 
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.fan_spped = 0
        self.isDisable = False
        self.ExtruderMax_temp = 0
        self.HeaterBedMax_temp = 0
        self.heater_bed_temp = 0
        self.h = 1
        self.extruder_temp = 0
        self.preheat_options = self._screen._config.get_preheat_options()
        for d in (self._printer.get_tools() + self._printer.get_heaters()):
            self.add_device(d)
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


        numPadIconExtruder = self._gtk.Image("calculator", self._screen.width *.04, self._screen.width *.04)
        numPadButtonExtruder = Gtk.Button(name ="speed-factor-button")
        numPadButtonExtruder.connect("clicked", self.open_numpad, 'extruder')
        numPadButtonExtruder.set_image(numPadIconExtruder)
        numPadButtonExtruder.set_always_show_image(True)
        
        #extruder
        self.extruderLabel = Gtk.Label("0.0° / 0.0°", name="temperature-label")
        extruderLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        extruderLabelBox.set_name("temperature-label-box")
        extruderLabelBox.set_valign(Gtk.Align.CENTER)
        extruderLabelBox.set_halign(Gtk.Align.CENTER)
        extruderLabelBox.pack_start(self.extruderLabel, False, False, 0)
        extruderLabelBox.pack_end(numPadButtonExtruder, False, False, 0)

        extruderLabelBoxEventBox = Gtk.EventBox()
        extruderLabelBoxEventBox.add(extruderLabelBox)
        extruderLabelBoxEventBox.connect("button-press-event", self.open_numpad_event, 'extruder')
        
        downIcon = self._gtk.Image("eksi", self._screen.width *.03, self._screen.width *.03)
        upIcon = self._gtk.Image("arti", self._screen.width *.03, self._screen.width *.03)
        
        upButton = Gtk.Button(name ="scale-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)
        upButton.connect("clicked", self.up_down_button_clicked, "extruder", "+")
        
        downButton = Gtk.Button(name ="scale-buttons-left")
        downButton.set_image(downIcon)
        downButton.set_always_show_image(True)
        downButton.connect("clicked", self.up_down_button_clicked, "extruder", "-")
       
        extruderInputBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        extruderInputBox.set_valign(Gtk.Align.CENTER)
        extruderInputBox.set_halign(Gtk.Align.CENTER)
        extruderInputBox.add(downButton)     
        extruderInputBox.add(extruderLabelBoxEventBox)
        extruderInputBox.add(upButton)  
        
        extruderImage = self._gtk.Image("extrudericon", self._screen.width *.07, self._screen.width *.07)
        
        extruderBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        extruderBox.add(extruderImage)
        extruderBox.add(extruderInputBox)
        
        #heatedBed
        numPadIconHeatedBed = self._gtk.Image("calculator", self._screen.width *.04, self._screen.width *.04)
        numPadButtonHeatedBed = Gtk.Button(name ="speed-factor-button")
        numPadButtonHeatedBed.connect("clicked", self.open_numpad, 'bed')
        numPadButtonHeatedBed.set_image(numPadIconHeatedBed)
        numPadButtonHeatedBed.set_always_show_image(True)
        
        self.heatedBedLabel = Gtk.Label("0.0° / 0.0°", name="temperature-label")
        heatedBedLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        heatedBedLabelBox.set_name("temperature-label-box")
        heatedBedLabelBox.set_valign(Gtk.Align.CENTER)
        heatedBedLabelBox.set_halign(Gtk.Align.CENTER)
        heatedBedLabelBox.add(self.heatedBedLabel)
        heatedBedLabelBox.pack_start(self.heatedBedLabel, False, False, 0)
        heatedBedLabelBox.pack_end(numPadButtonHeatedBed, False, False, 0)
        
        heatedBedLabelBoxEventBox = Gtk.EventBox()
        heatedBedLabelBoxEventBox.add(heatedBedLabelBox)
        heatedBedLabelBoxEventBox.connect("button-press-event", self.open_numpad_event, 'bed')
   
        
        downIcon = self._gtk.Image("eksi", self._screen.width *.03, self._screen.width *.03)
        upIcon = self._gtk.Image("arti", self._screen.width *.03, self._screen.width *.03)
        
        upButton = Gtk.Button(name ="scale-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)
        upButton.connect("clicked", self.up_down_button_clicked, "heatedBed", "+")
        
        downButton = Gtk.Button(name ="scale-buttons-left")
        downButton.set_image(downIcon)
        downButton.set_always_show_image(True)
        downButton.connect("clicked", self.up_down_button_clicked, "heatedBed", "-")
       
        heatedBedInputBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        heatedBedInputBox.set_valign(Gtk.Align.CENTER)
        heatedBedInputBox.set_halign(Gtk.Align.CENTER)
        heatedBedInputBox.add(downButton)     
        heatedBedInputBox.add(heatedBedLabelBoxEventBox)
        heatedBedInputBox.add(upButton)  
        
        heatedBedImage = self._gtk.Image("tablaicon", self._screen.width *.07, self._screen.width *.07)
        
        heatedBedBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        heatedBedBox.add(heatedBedImage)
        heatedBedBox.add(heatedBedInputBox)

        extruderHeatedBedBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        extruderHeatedBedBox.set_valign(Gtk.Align.CENTER)
        extruderHeatedBedBox.set_halign(Gtk.Align.CENTER)
        extruderHeatedBedBox.pack_start(extruderBox, False, True, 0)
        extruderHeatedBedBox.pack_start(heatedBedBox, False, True, 0)
        
        
        increaseLabel = Gtk.Label(_("Select + - increase value"), name="increase-label")
        
       
        self.buttons = {"1": Gtk.Button("1", name ="increase-button"),
                        "5": Gtk.Button("5", name ="increase-button"),
                        "10": Gtk.Button("10", name ="increase-button"),
                        "20": Gtk.Button("20", name ="increase-button"),
                        "50": Gtk.Button("50", name ="increase-button")
        }
        self.constant = 10
        self.buttons[f"{1}"].connect("clicked", self.change_temp_constant, 1)
        self.buttons[f"{5}"].connect("clicked", self.change_temp_constant, 5)
        self.buttons[f"{10}"].connect("clicked", self.change_temp_constant, 10)
        self.buttons[f"{20}"].connect("clicked", self.change_temp_constant, 20)
        self.buttons[f"{50}"].connect("clicked", self.change_temp_constant, 50)
        self.buttons[f"{10}"].get_style_context().add_class("increase-button-active")

        increaseButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        increaseButtonBox.set_spacing(-10)
        increaseButtonBox.set_valign(Gtk.Align.CENTER)
        #increaseButtonBox.set_halign(Gtk.Align.CENTER)
        increaseButtonBox.pack_start(self.buttons[f"{1}"], True, False, 0)
        increaseButtonBox.pack_start(self.buttons[f"{5}"], True, False, 0)
        increaseButtonBox.pack_start(self.buttons[f"{10}"], True, False, 0)
        increaseButtonBox.pack_start(self.buttons[f"{20}"], True, False, 0)
        increaseButtonBox.pack_start(self.buttons[f"{50}"], True, False, 0)
        
        increaseBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        increaseButtonBox.set_halign(Gtk.Align.CENTER)
        increaseBox.pack_start(increaseLabel, True, False, 0)
        increaseBox.pack_start(increaseButtonBox, True, False, 0)
        
        progressBarBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        progressBarBox.set_valign(Gtk.Align.CENTER)
        progressBarBox.set_name("fan-speed-progress-box")
        fanSpeedLabel = Gtk.Label(_("Fan Speed"), name="number-label")
        
        self.scale = Gtk.Scale()
        self.scale.set_range(0, 100)
        self.scale.set_value(0)
        self.scale.set_increments(1, 1)
        self.scale.set_digits(1)
        self.scale.set_draw_value(False)
        self.scale.set_size_request(-1, 1)
        self.scale.connect("value-changed", self.on_scale_changed, 1)
        context = self.scale.get_style_context()
        context.add_class("fan-speed")
        
        self.fanSpeedInput = Gtk.Label("0", name="fan-speed-input-label")
        fanSpeedInputBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        fanSpeedInputBox.set_valign(Gtk.Align.CENTER)
        fanSpeedInputBox.set_halign(Gtk.Align.CENTER)
        fanSpeedInputBox.add(self.fanSpeedInput)
        
        progressBarBox.pack_start(fanSpeedLabel, False, False, 0)
        progressBarBox.pack_start(self.scale, True, True, 20)
        progressBarBox.pack_start(fanSpeedInputBox, False, False, 0)
        
        self.plaButton = Gtk.Button(_("Preheat PLA"), name ="pre-temperature-button")
        self.plaButton.connect("clicked", self.set_temperature,  'PLA')
        self.absButton = Gtk.Button(_("Preheat ABS"), name ="pre-temperature-button")
        self.absButton.connect("clicked", self.set_temperature,  'ABS')
        self.coolDownButton = Gtk.Button(_("Cooldown"), name ="pre-temperature-button")
        self.coolDownButton.connect("clicked", self.set_temperature,  'cooldown')
        
        preButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        preButtonBox.pack_start(self.plaButton, True, False, 0)
        preButtonBox.pack_start(self.absButton, True, False, 0)
        preButtonBox.pack_start(self.coolDownButton, True, False, 0)
        
        contentBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        contentBox.set_halign(Gtk.Align.CENTER)
        contentBox.pack_start(extruderHeatedBedBox, False, True, 10)
        contentBox.pack_start(increaseBox, False, False, 20)
        contentBox.pack_start(progressBarBox, False, False, 0)
        contentBox.pack_start(preButtonBox, False, False, 20)
        
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_vexpand(True)
        main.pack_start(contentBox, False, True, 0)
        main.pack_end(BottomMenu(self, True), False, True, 0)
        
 
        self.content.add(main)
        
    def open_numpad(self, widget, type):
        
        dialog = KeyPadNew(self)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            resp = dialog.resp
            if type == 'extruder':
                self.change_extruder_temperature(int(resp))
            else:
                self.change_bed_temperature(int(resp))
            
            
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
       
        dialog.destroy()

    def open_numpad_event(self, widget, event, type):
        
        dialog = KeyPadNew(self)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            resp = dialog.resp
            if type == 'extruder':
                self.change_extruder_temperature(int(resp))
            else:
                self.change_bed_temperature(int(resp))
            
            
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
       
        dialog.destroy()
    def change_temp_constant(self, widget, constant):
        logging.info(f"### Temp constant {constant}")
        self.buttons[f"{self.constant}"].get_style_context().remove_class("increase-button-active")
        self.buttons[f"{constant}"].get_style_context().add_class("increase-button-active")
        self.constant = constant

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
                if heater.startswith('extruder'):
                    if self.validate(heater, target, max_temp):
                        self._screen._ws.klippy.set_tool_temp(self._printer.get_tool_number(heater), target)
                        self.extruderLabel.set_label(str(round(self.extruder_temp,1)) + f"° / {target}°")
                elif heater.startswith('heater_bed'):
                    if target is None:
                        with contextlib.suppress(KeyError):
                            target = self.preheat_options[setting]["bed"]
                    if self.validate(heater, target, max_temp):
                        self._screen._ws.klippy.set_bed_temp(target)
                        self.heatedBedLabel.set_label(str(round(self.heater_bed_temp,1)) + f"° / {target}°")
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
        if type(self._printer.get_config_section('extruder')) != bool:
            self.ExtruderMax_temp = float(self._printer.get_config_section('extruder')['max_temp'])    
        if type(self._printer.get_config_section('heater_bed')) != bool:
            self.HeaterBedMax_temp = float(self._printer.get_config_section('heater_bed')['max_temp'])
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
   
    def on_scale_changed(self, scale, valuee):
        # Ölçek değeri değiştiğinde çağrılır
        value = int(scale.get_value())
        self.set_fan_speed(value)
       
        self.fanSpeedInput.set_label('{:.0f}'.format(value) + '%')
    
    def set_fan_speed(self, value):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.set_fan_speed(value))
    
    def process_update(self, action, data):
        # if self._printer.state == 'error' or self._printer.state == 'shutdown' or self._printer.state ==  'disconnected':
        #     page_url = 'co_print_home_not_connected_screen'
        #     self._screen.show_panel(page_url, page_url, "Language", 1, False)
            
        if self._printer.state != 'error' :
            
           
            heater_bed_array = self._printer.get_temp_store('heater_bed')
            if(heater_bed_array):
                self.heater_bed_temp = heater_bed_array['temperatures'][-1]
                self.heater_bed_temp_target = heater_bed_array['targets'][-1]
                if(self.isDisable == False):
                    self.heatedBedLabel.set_label(str(round(self.heater_bed_temp,1)) + f"° / {self.heater_bed_temp_target}°")
            else:
                if(self.isDisable == False):
                    self.heatedBedLabel.set_label(str(-1) + f"° / {self.HeaterBedMax_temp}°")
            extruder_array = self._printer.get_temp_store('extruder')
            if(extruder_array):
                self.extruder_temp = extruder_array['temperatures'][-1]
                self.extruder_temp_target = extruder_array['targets'][-1]
                if(self.isDisable == False):
                    self.extruderLabel.set_label(str(round(self.extruder_temp,1)) + f"° / {self.extruder_temp_target}°")
            else:
                if(self.isDisable == False):
                    self.extruderLabel.set_label(str(-1) + f"° / {self.extruder_temp_target}°")
            if 'fan' in data and self.fan_spped != data['fan']['speed']:
                self.fan_spped = data['fan']['speed'] 
                self.scale.set_value(self.fan_spped*100)
                #self.fanSpeed_widget.updateValue(self.fan_spped*100, str(int(self.fan_spped*100)))
           
    def change_bed_temperature(self, temp):
        max_temp = float(self._printer.get_config_section('heater_bed')['max_temp'])
        if self.validate('heater_bed', temp, max_temp):
            self._screen._ws.klippy.set_bed_temp(temp)
            if self.isDisable ==False:
                self.start_timer()
            self.heatedBedLabel.set_label(str(round(self.heater_bed_temp,1)) + f"° / {temp}°")


    def start_timer(self):
        self.isDisable = True
        """ Start the timer. """
        self.timeout_id = GLib.timeout_add(10000, self.on_timeout, None)
        

    def on_timeout(self, *args, **kwargs):
        self.isDisable = False
        
        self.timeout_id = None
        #self.destroy()
        return False      

    def change_extruder_temperature(self,temp):
        
        max_temp = float(self._printer.get_config_section('extruder')['max_temp'])
        if self.validate('extrude', temp, max_temp):

            self._screen._ws.klippy.set_tool_temp(self._printer.get_tool_number('extruder'), temp)
            if self.isDisable ==False:
                self.start_timer()
            self.extruderLabel.set_label(str(round(self.extruder_temp,1)) + f"° / {temp}°")

    def del_obj(self):
        self.isDisable = False


    def up_down_button_clicked(self, widget, tempType , direction):
        value =0
        if(direction =="+"):
            if(tempType== "extruder"):
                value = self.extruder_temp_target + self.constant
            else:
                value = self.heater_bed_temp_target + self.constant
        else:
            if(tempType== "extruder"):
                value = self.extruder_temp_target - self.constant
            else:
                value = self.heater_bed_temp_target - self.constant

        if (value < 0):
            value = 0
        if(tempType == 'extruder'):
            self.change_extruder_temperature(value)
              
        else:
            self.change_bed_temperature(value)
                
                
    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_printing_selection_port", "co_print_printing_selection_port", None, 2)
        
   
