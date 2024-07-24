import contextlib
import logging
#import os
import time
import gi
from ks_includes.widgets.keypad_new import KeyPadNew
from ks_includes.widgets.movebuttonboxtext import MoveButtonBoxText
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.keypad import Keypad
from ks_includes.widgets.movebuttonbox import MoveButtonBox
from ks_includes.widgets.zaxis import zAxis
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf
from ks_includes.screen_panel import ScreenPanel

# def create_panel(*args):
#     return CoPrintExtrudersScreen(*args)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# class CoPrintExtrudersScreen(ScreenPanel, metaclass=Singleton):
class Panel(ScreenPanel, metaclass=Singleton):
    active_heater = None
    extruderChanged = False
    temp_extruder_temp = 0
    
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.extruders = self._printer.extruders
        self.current_time_millis = int(round(time.time() * 1000))
        self.ExtruderMax_temp = 0
        self.distance = 50
        self.preheat_options = self._screen._config.get_preheat_options()
        self.h = 1
        self.grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=10,
                         row_spacing=10)
        self.sliderBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.sliderBox.set_halign(Gtk.Align.CENTER)
        self.startIndex = 0
        for extruder in self.extruders:

            extruder['Image'] = self._gtk.Image(extruder['Icon'], self._gtk.content_width * .10 , self._gtk.content_height * .10)
            extruder['RadioButton'] = self._gtk.Image('passive', self._gtk.content_width * .04 , self._gtk.content_height * .04)

            alignment = Gtk.Alignment.new(1, 0, 0, 0)
            alignment.add(extruder['RadioButton'])

            extruderBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            extruderBox.set_name("extruder-extruder-select-box")
            extruderBox.pack_start(alignment, False, False, 5)
            extruderBox.pack_start(extruder['Image'], False, True, 5)

            eventBox = Gtk.EventBox()
            eventBox.add(extruderBox)
            extruder['EventBox'] = Gtk.Frame(name= "extrude")
            extruder['EventBox'].add(eventBox)

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

        self.content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.content_box.set_hexpand(True)
        self.content_box.set_halign(Gtk.Align.CENTER)
        self.content_box.set_valign(Gtk.Align.CENTER)
        self.content_box.pack_start(self.generate_grid_box(), False, True, 0)
        self.content_box.pack_start(self.generate_extruder_box(), False, True, 0)
        self.content_box.pack_start(self.generate_move_button_box(), False, True, 0)
        self.content_box.pack_start(self.generate_extrusion_speed_button_box(), False, True, 0)
        self.content_box.pack_start(self.generate_selected_extruder_button_box(), False, True, 0)

        self.main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main.set_vexpand(True)
        self.main.pack_start(self.content_box, False, False, 0)
        self.main.pack_end(BottomMenu(self, True), False, True, 0)

        self.content.add(self.main)

    def generate_grid_box(self):
        prevIcon = self._gtk.Image("moveust", 45, 45)
        self.prevButton = Gtk.Button(name ="prev-next-button")
        self.prevButton.add(prevIcon)
        self.prevButton.connect("clicked", self.show_prev_page)
        self.prevButton.set_always_show_image (True)
        prevButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        prevButtonBox.set_halign(Gtk.Align.CENTER)
        prevButtonBox.pack_start(self.prevButton, False, False, 0)

        nextIcon = self._gtk.Image("movealt", 45, 45)
        self.nextButton = Gtk.Button(name ="prev-next-button")
        self.nextButton.add(nextIcon)
        self.nextButton.connect("clicked", self.show_next_page)
        self.nextButton.set_always_show_image (True)
        nextButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        nextButtonBox.set_halign(Gtk.Align.CENTER)
        nextButtonBox.pack_start(self.nextButton, False, False, 0)

        selectableBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        selectableBox.set_name("selectable-box")
        selectableBox.pack_start(self.generateGrid(), False, False, 0)

        fixed = Gtk.Fixed()
        fixed.set_valign(Gtk.Align.START)
        fixed.set_halign(Gtk.Align.START)
        fixed.put(selectableBox, 5, 30)
        fixed.put(prevButtonBox, 60, 0)
        fixed.put(nextButtonBox, 60, 330)

        connectedExtruders = Gtk.Label(_("Select Controlled \n Extruder"), name="move-label")
        connectedExtrudersBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        connectedExtrudersBox.set_halign(Gtk.Align.CENTER)
        connectedExtruders.set_justify(Gtk.Justification.CENTER)
        connectedExtrudersBox.add(connectedExtruders)
        gridBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(connectedExtrudersBox)
        gridBox.add(fixed)
        return gridBox

    def generate_extruder_box(self):
        if self._printer.selectedExtruder == "":
            self.extruderImage = self._gtk.Image("ext_free", self._screen.width *.07, self._screen.width *.07)
        else :
            for extruder in self.extruders:
                if extruder['Extrude'] == self._printer.selectedExtruder:
                    self.extruderImage = self._gtk.Image(extruder['Icon'], self._gtk.content_width * .07 , self._gtk.content_height * .07)
        switchWithImageBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        switchWithImageBox.set_halign(Gtk.Align.CENTER)
        switchWithImageBox.add(self.extruderImage)

        extrudeBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        extrudeBox.set_valign(Gtk.Align.CENTER)
        extrudeBox.pack_start(switchWithImageBox, False, False, 0)

        numPadIcon = self._gtk.Image("calculator", self._screen.width *.04, self._screen.width *.04)
        numPadButton = Gtk.Button(name ="speed-factor-button")
        numPadButton.set_image(numPadIcon)
        numPadButton.set_always_show_image(True)
        numPadButton.connect("clicked", self.open_numpad)

        self.distanceLabel = Gtk.Label(self.distance, name="number-label")

        numberLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        numberLabelBox.set_valign(Gtk.Align.CENTER)
        numberLabelBox.set_halign(Gtk.Align.CENTER)
        numberLabelBox.set_name("number-label-box")
        numberLabelBox.add(self.distanceLabel)

        InputBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        InputBox.set_valign(Gtk.Align.CENTER)
        InputBox.pack_start(numberLabelBox, True, True, 0)
        InputBox.pack_end(numPadButton, True, True, 0)
        extrudeBox.pack_start(InputBox, False, False, 0)

        Extrude = zAxis(self, "", False)
        ExtrudeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ExtrudeBox.pack_start(Extrude, False, False, 0)
        ExtrudeBox.set_halign(Gtk.Align.CENTER)

        extrudeBox.pack_start(ExtrudeBox, False, False, 0)

        extrudeBox_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        extrudeBox_box.set_halign(Gtk.Align.CENTER)
        extrudeBox_box.set_name("move-page-common-box")
        extrudeBox_box.pack_start(extrudeBox, False, False, 0)
        return extrudeBox_box

    def generate_move_button_box(self):
        moveButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        moveButtonBox.set_halign(Gtk.Align.CENTER)
        moveButtonBox.set_name("move-page-common-box")
        moveButtons = MoveButtonBox(_("Extruder Movement (mm)"), 100, 50, 25, 10, "move-button", self)
        moveButtonBox.add(moveButtons)
        return moveButtonBox

    def generate_extrusion_speed_button_box(self):

        extrusionSpeedButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        extrusionSpeedButtonBox.set_halign(Gtk.Align.CENTER)
        extrusionSpeedButtonBox.set_name("move-page-common-box")
        extrusionSpeedButtons = MoveButtonBoxText(_("Extrusion Speed (mm)"), _("Slow"), _("Normal"), _("High"), "50", "extrusion-speed-button", self)
        extrusionSpeedButtonBox.add(extrusionSpeedButtons)
        return extrusionSpeedButtonBox

    def generate_selected_extruder_button_box(self):

        self.selectedExtruderLabel = Gtk.Label("0.0° / 0.0°", name="selected-extuder-label")
        selectedExtruderImage = self._gtk.Image("extrudericon", self._screen.width *.03, self._screen.width *.03)
        selectedExtruderLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        selectedExtruderLabelBox.set_name("selected-extuder-box")
        selectedExtruderLabelBox.set_valign(Gtk.Align.CENTER)
        selectedExtruderLabelBox.pack_start(selectedExtruderImage, True, False, 0)
        selectedExtruderLabelBox.pack_start(self.selectedExtruderLabel, True, False, 0)

        self.plaButton = Gtk.Button(_("Preheat PLA"), name ="selected-extuder-button")
        self.plaButton.connect("clicked", self.set_temperature,  'PLA')
        self.absButton = Gtk.Button(_("Preheat ABS"), name ="selected-extuder-button")
        self.absButton.connect("clicked", self.set_temperature,  'ABS')
        self.coolDownButton = Gtk.Button(_("Cooldown"), name ="selected-extuder-button")
        self.coolDownButton.connect("clicked", self.set_temperature,  'cooldown')
        self.disableStepperButton = Gtk.Button(_("Disable Stepper"), name ="selected-extuder-button")
        self.disableStepperButton.connect("clicked", self.disable_motors)

        self.connectedExtruder = Gtk.Label(self._printer.selectedExtruder, name="connected-extruder-label")
        connectedExtruderBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        connectedExtruderBox.set_halign(Gtk.Align.START)
        connectedExtruderBox.add(self.connectedExtruder)

        selectedExtruderButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        selectedExtruderButtonBox.pack_start(connectedExtruderBox, True, False, 0)
        selectedExtruderButtonBox.pack_start(selectedExtruderLabelBox, True, True, 0)
        selectedExtruderButtonBox.pack_start(self.plaButton, True, False, 0)
        selectedExtruderButtonBox.pack_start(self.absButton, True, False, 0)
        selectedExtruderButtonBox.pack_start(self.coolDownButton, True, False, 0)
        selectedExtruderButtonBox.pack_start(self.disableStepperButton, True, False, 0)
        return selectedExtruderButtonBox

    def show_next_page(self, widget):
        self.startIndex = self.startIndex +4
        if self.startIndex > 16:
            self.startIndex = 16
        self.generateGrid()

    def show_prev_page(self, widget):
        if self.startIndex <= 4:
            self.startIndex = 0
        else:
            self.startIndex = (self.startIndex - 4)
        self.generateGrid()

    def generateGrid(self):
        if self.sliderBox.get_children() != None:
            for child in self.sliderBox.get_children():
                self.sliderBox.remove(child)
        grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=10,
                         row_spacing=10)
        row = 0
        count = 0
        for extruder in self.extruders[self.startIndex: self.startIndex+4]:
            extruder['Image'] = self._gtk.Image(extruder['Icon'], self._gtk.content_width * .10 , self._gtk.content_height * .10)
            if extruder['RadioButtonStatus']:
                extruder['RadioButton'] = self._gtk.Image('active', self._gtk.content_width * .04 , self._gtk.content_height * .04)
            else:
                extruder['RadioButton'] = self._gtk.Image('passive', self._gtk.content_width * .04 , self._gtk.content_height * .04)
            alignment = Gtk.Alignment.new(1, 0, 0, 0)
            alignment.add(extruder['RadioButton'])
            extruderBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            extruderBox.set_name("extruder-extruder-select-box")
            extruderBox.pack_start(alignment, False, False, 5)
            extruderBox.pack_start(extruder['Image'], False, True, 5)
            eventBox = Gtk.EventBox()
            eventBox.add(extruderBox)
            extruder['EventBox'] = Gtk.Frame(name= "extrude")
            extruder['EventBox'].add(eventBox)
            if extruder['RadioButtonStatus']:
                extruder['EventBox'].connect("button-press-event", self.chanceExtruder, extruder['Extrude'])
            if extruder['Extrude'] != self._printer.selectedExtruder:
                extruder['EventBox'].get_style_context().remove_class("extrude-active")
            else:
                extruder['EventBox'].get_style_context().add_class("extrude-active")
            grid.attach(extruder['EventBox'], count, row, 1, 1)
            count += 1
            if count % 2 == 0:
                count = 0
                row += 1

        gridBox = Gtk.Box()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)
        self.sliderBox.pack_start(gridBox,False, False,0)
        self.sliderBox.show_all()
        return self.sliderBox or  True

    def open_numpad(self, widget):
        dialog = KeyPadNew(self)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            if(self.distance):
                self.distance = int(dialog.resp)
            if(self.distanceLabel):
                self.distanceLabel.set_label(dialog.resp)
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        dialog.destroy()   

    def disable_motors(self, widget):
        self._screen._ws.klippy.gcode_script(
            "M18"  # Disable motors
        )

    def chanceExtruder(self,eventBox ,  gparam, extruder):
        for i, item in enumerate(self.extruders):
            if item['Extrude'] != extruder:
                item['EventBox'].get_style_context().remove_class("extrude-active")
            else:
                item['EventBox'].get_style_context().add_class("extrude-active")
                #self.connectedExtruder.set_label(extruder)
                svg_file = f"styles/z-bolt/images/{self.extruders[i]['Icon']}.png"
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(svg_file, self._gtk.content_width * .12 , self._gtk.content_height * .12)
                self.extruderImage.set_from_pixbuf(pixbuf)
                self._screen._ws.klippy.gcode_script("T" + str(i))

    def process_update(self, action, data):
        if self._printer.state != 'error' :
            extruder_list = self._printer.get_tools()
            for extruder in extruder_list:
                if self._printer.data[extruder]["motion_queue"] != None:
                    if action == "notify_gcode_response" and data.startswith("// ") and data.endswith("'extruder'"):
                        new_extruder = 'extruder_stepper ' + (data.split()[2].strip("'"))
                        if self._printer.selectedExtruder != new_extruder:
                            self._printer.selectedExtruder = new_extruder
                            self.extruderChanged = False
                            self.connectedExtruder.set_label(self._printer.selectedExtruder)
            extrude = self._printer.get_config_section(self._printer.selectedExtruder)
            if (extrude):
                self.ExtruderMax_temp = float(self._printer.get_config_section('extruder')['max_temp'])
            extruder_temp = 0
            extruder_array = self._printer.get_temp_store(self._printer.data["toolhead"]["extruder"])
            if(extruder_array):
                extruder_temp = extruder_array['temperatures'][-1]
                if(self.temp_extruder_temp != extruder_temp):
                    self.temp_extruder_temp = extruder_temp
                    self.extruder_temp_target = extruder_array['targets'][-1]
                    self.temp_extruder_temp_target = self.extruder_temp_target
                    self.selectedExtruderLabel.set_label(str(round(extruder_temp,1)) + f"° / {self.extruder_temp_target}°")
            else:
                extruder_temp = -1
                if(self.temp_extruder_temp != extruder_temp):
                    self.temp_extruder_temp = extruder_temp
                    self.selectedExtruderLabel.set_label(str(round(extruder_temp,1)) + f"° / {0}°")
        if(self.extruderChanged == False):
            i = 0
            for d in (self._printer.get_tools() + self._printer.get_heaters()):
                self.add_device(d)

            self.extruderChanged = True
            for extruder in self._printer.get_tools():
                if extruder != 'extruder':
                    svg_file = "styles/z-bolt/images/active.svg"
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(svg_file, self._gtk.content_width * .04 , self._gtk.content_height * .04)
                    self.extruders[i]['RadioButtonStatus'] = True
                    self.extruders[i]['RadioButton'].set_from_pixbuf(pixbuf)
                    if self.extruders[i]['Extrude'] is None:
                        self.extruders[i]['EventBox'].connect("button-press-event", self.chanceExtruder, extruder)
                    self.extruders[i]['Extrude'] = extruder
                    if self.extruders[i]['Extrude'] != self._printer.selectedExtruder:
                        self.extruders[i]['EventBox'].get_style_context().remove_class("extrude-active")
                    else:
                        self.extruders[i]['EventBox'].get_style_context().add_class("extrude-active")
                        svg_file = f"styles/z-bolt/images/{self.extruders[i]['Icon']}.png"
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(svg_file, self._gtk.content_width * .12 , self._gtk.content_height * .12)
                        self.extruderImage.set_from_pixbuf(pixbuf)
                    i += 1


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
            logging.info(f"Seselecting {self.devices}")
        return

    def set_temperature(self, widget, setting):
        self.extruderChanged = False
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
                elif heater.startswith('heater_bed'):
                    if target is None:
                        with contextlib.suppress(KeyError):
                            target = self.preheat_options[setting]["bed"]
                    if self.validate(heater, target, max_temp):
                        self._screen._ws.klippy.set_bed_temp(target)
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

    def del_obj(self):
        self.extruderChanged = False

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
        if self._printer.selectedExtruder != "" and self._printer.get_config_section(self._printer.selectedExtruder):
            self.ExtruderMax_temp = float(self._printer.get_config_section('extruder')['max_temp'])
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


    def reinit(self):
        self.connectedExtruder.set_label(self._printer.selectedExtruder)
        self.generateGrid()
