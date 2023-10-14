import logging
import os
import time
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.keypad import Keypad
from ks_includes.widgets.progressbar import ProgressBar
from ks_includes.widgets.mainbutton import MainButton
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf
from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintHomeScreen(*args)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CoPrintHomeScreen(ScreenPanel, metaclass=Singleton):
    selectedExtruder = ""
    active_heater = None
    extruderChanged = False
    getToolsActivated = False
    desiredTemp = 1
    temp_extruder_temp = 0
    temp_heater_bed_temp = 0
    extruders = [
            {'Name': '1', 'Icon': 'ext_1', 'Image': None, 'Extrude': None, 'EventBox': None, 'RadioButton': None},
            {'Name': '2', 'Icon': 'ext_2', 'Image': None, 'Extrude': None, 'EventBox': None, 'RadioButton': None},
            {'Name': '3', 'Icon': 'ext_3', 'Image': None, 'Extrude': None, 'EventBox': None, 'RadioButton': None},
            {'Name': '4', 'Icon': 'ext_4', 'Image': None, 'Extrude': None, 'EventBox': None, 'RadioButton': None},
            {'Name': '5', 'Icon': 'ext_5', 'Image': None, 'Extrude': None, 'EventBox': None, 'RadioButton': None},
            {'Name': '6', 'Icon': 'ext_6', 'Image': None, 'Extrude': None, 'EventBox': None, 'RadioButton': None},
            {'Name': '7', 'Icon': 'ext_7', 'Image': None, 'Extrude': None, 'EventBox': None, 'RadioButton': None},
            {'Name': '8', 'Icon': 'ext_8', 'Image': None, 'Extrude': None, 'EventBox': None, 'RadioButton': None},
            ]

    def __init__(self, screen, title):
        super().__init__(screen, title)
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
        self.connectedExtruder = Gtk.Label("Extruder 1", name="connected-extruder-label")
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


        E1Button = Gtk.ColorButton(name="e1-button")
        E1CurrentColor = Gdk.RGBA()
        E1CurrentColor.parse("#F7BA17")
        E1Button.set_rgba(E1CurrentColor)
        E1Button.set_title("Select a color")
        E1Button.connect('color-set', self.on_color_set)
        E1Button.get_style_context().add_class("DSFGSDFHSH")
        E1ButtonLabel = Gtk.Label("E1", name="e1-button-label")
        E1Button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        E1Button_box.set_name("color-button-box")
        E1Button_box.set_halign(Gtk.Align.CENTER)
        E1Button_box.pack_start(E1ButtonLabel, False, False, 0)
        E1Button_box.pack_start(E1Button, False, False, 0)


        E2Button = Gtk.ColorButton(name ="e1-button")
        E2CurrentColor = Gdk.RGBA()
        E2CurrentColor.parse("#178BF7")
        E2Button.set_rgba(E2CurrentColor)
        E2Button.set_title("Select a color")
        E2Button.connect('color-set', self.on_color_set)
        E2ButtonLabel = Gtk.Label("E2", name="e1-button-label")
        E2Button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        E2Button_box.set_name("color-button-box")
        E2Button_box.set_halign(Gtk.Align.CENTER)
        E2Button_box.pack_start(E2ButtonLabel, False, False, 0)
        E2Button_box.pack_start(E2Button, False, False, 0)


        E3Button = Gtk.ColorButton(name ="e1-button")
        E3CurrentColor = Gdk.RGBA()
        E3CurrentColor.parse("#BD17F7")
        E3Button.set_rgba(E3CurrentColor)
        E3Button.set_title("Select a color")
        E3Button.connect('color-set', self.on_color_set)
        E3ButtonLabel = Gtk.Label("E3", name="e1-button-label")
        E3Button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        E3Button_box.set_name("color-button-box")
        E3Button_box.set_halign(Gtk.Align.CENTER)
        E3Button_box.pack_start(E3ButtonLabel, False, False, 0)
        E3Button_box.pack_start(E3Button, False, False, 0)


        E4Button = Gtk.ColorButton(name ="e1-button")
        E4CurrentColor = Gdk.RGBA()
        E4CurrentColor.parse("#17F7EA")
        E4Button.set_rgba(E4CurrentColor)
        E4Button.set_title("Select a color")
        E4Button.connect('color-set', self.on_color_set)
        E4ButtonLabel = Gtk.Label("E4", name="e1-button-label")
        E4Button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        E4Button_box.set_name("color-button-box")
        E4Button_box.set_halign(Gtk.Align.CENTER)
        E4Button_box.pack_start(E4ButtonLabel, False, False, 0)
        E4Button_box.pack_start(E4Button, False, False, 0)


        E5Button = Gtk.ColorButton(name ="e1-button")
        E5CurrentColor = Gdk.RGBA()
        E5CurrentColor.parse("#F74D17")
        E5Button.set_rgba(E5CurrentColor)
        E5Button.set_title("Select a color")
        E5Button.connect('color-set', self.on_color_set)
        E5ButtonLabel = Gtk.Label("E5", name="e1-button-label")
        E5Button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        E5Button_box.set_name("color-button-box")
        E5Button_box.set_halign(Gtk.Align.CENTER)
        E5Button_box.pack_start(E5ButtonLabel, False, False, 0)
        E5Button_box.pack_start(E5Button, False, False, 0)


        E6Button = Gtk.ColorButton(name ="e1-button")
        E6CurrentColor = Gdk.RGBA()
        E6CurrentColor.parse("#FFFBF1")
        E6Button.set_rgba(E6CurrentColor)
        E6Button.set_title("Select a color")
        E6Button.connect('color-set', self.on_color_set)
        E6ButtonLabel = Gtk.Label("E6", name="e1-button-label")
        E6Button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        E6Button_box.set_name("color-button-box")
        E6Button_box.set_halign(Gtk.Align.CENTER)
        E6Button_box.pack_start(E6ButtonLabel, False, False, 0)
        E6Button_box.pack_start(E6Button, False, False, 0)


        E7Button = Gtk.ColorButton(name ="e1-button")
        E7CurrentColor = Gdk.RGBA()
        E7CurrentColor.parse("#332FD0")
        E7Button.set_rgba(E7CurrentColor)
        E7Button.set_title("Select a color")
        E7Button.connect('color-set', self.on_color_set)
        E7ButtonLabel = Gtk.Label("E7", name="e1-button-label")
        E7Button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        E7Button_box.set_name("color-button-box")
        E7Button_box.set_halign(Gtk.Align.CENTER)
        E7Button_box.pack_start(E7ButtonLabel, False, False, 0)
        E7Button_box.pack_start(E7Button, False, False, 0)


        E8Button = Gtk.ColorButton(name ="e1-button")
        E8CurrentColor = Gdk.RGBA()
        E8CurrentColor.parse("#28DF99")
        E8Button.set_rgba(E8CurrentColor)
        E8Button.set_title("Select a color")
        E8Button.connect('color-set', self.on_color_set)
        E8ButtonLabel = Gtk.Label("E8", name="e1-button-label")
        E8Button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        E8Button_box.set_halign(Gtk.Align.CENTER)
        E8Button_box.set_name("color-button-box")
        E8Button_box.pack_start(E8ButtonLabel, False, False, 0)
        E8Button_box.pack_start(E8Button, False, False, 0)

        gridBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        gridBox.set_halign(Gtk.Align.CENTER)

        gridLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        gridLabelBox.set_name("extruder-heatedbad-label-box")
        gridLabelBox.set_valign(Gtk.Align.CENTER)
        gridLabel = Gtk.Label(_("Multi Filament Printing"), name="connected-extruder-label")
        gridLabel.set_justify(Gtk.Justification.LEFT)
        gridLabelBox.pack_start(gridLabel, False, False, 0)
        gridBox.pack_start(gridLabelBox, False, False, 0)
        gridBox.pack_start(grid, False, False, 0)

        multiFlamet_grid = Gtk.Grid()
        multiFlamet_grid.set_name("home-multifilament-select-box")
        multiFlamet_grid.set_column_spacing(5)
        multiFlamet_grid.set_row_spacing(5)
        multiFlamet_grid.set_column_homogeneous(True)
        multiFlamet_grid.attach(E1Button_box, 0, 1, 1, 1)
        multiFlamet_grid.attach(E2Button_box, 0, 2, 1, 1)
        multiFlamet_grid.attach(E3Button_box, 0, 3, 1, 1)
        multiFlamet_grid.attach(E4Button_box, 0, 4, 1, 1)
        multiFlamet_grid.attach(E5Button_box, 0, 5, 1, 1)
        multiFlamet_grid.attach(E6Button_box, 0, 6, 1, 1)
        multiFlamet_grid.attach(E7Button_box, 0, 7, 1, 1)
        multiFlamet_grid.attach(E8Button_box, 0, 8, 1, 1)



        changeColorBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        changeColorBox.set_name("extruder-heatedbad-label-box")
        changeColorBox.set_valign(Gtk.Align.CENTER)
        changeColorLabel = Gtk.Label(_("Change Color"), name="connected-extruder-label")
        changeColorLabel.set_justify(Gtk.Justification.CENTER)
        changeColorBox.pack_start(changeColorLabel, False, False, 0)

        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_kinetic_scrolling(True)
        scroll.get_overlay_scrolling()
        scroll.set_hexpand(True)
        scroll.set_vexpand(True)
        scroll.add(multiFlamet_grid)

        multiFilamentGridBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        multiFilamentGridBox.pack_start(changeColorBox, False, False, 0)
        multiFilamentGridBox.pack_start(scroll, True, True, 0)

        multiFlamentButton_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        multiFlamentButton_box.add(gridBox)
        multiFlamentButton_box.add(multiFilamentGridBox)

        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        left_box.pack_start(connectedExtruderBox, False, False, 0)
        left_box.pack_start(connectedHeatedBox, False, False, 0)

        left_box.pack_end(multiFlamentButton_box, True, True, 0)

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
        right_box.pack_start(menuGrid, False, True, 0)


        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main_box.pack_start(left_box, True, True, 0)
        main_box.pack_start(right_box, True, True, 0)
        main_box.set_vexpand(True)
        #main_box.set_valign(Gtk.Align.CENTER)

        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(main_box, True, True, 0)
        page.pack_end(menu, False, True, 0)


        self.content.add(page)



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

    def process_update(self, action, data):


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

            if self.selectedExtruder != self._printer.data["toolhead"]["extruder"]:
                self.extruderChanged = False
                self.selectedExtruder = self._printer.data["toolhead"]["extruder"]
                self.connectedExtruder.set_label(self._printer.data["toolhead"]["extruder"])

            extrude = self._printer.get_config_section(self.selectedExtruder)
            if(extrude):
                self.ExtruderMax_temp = float(extrude['max_temp'])

            if(self.extruderChanged == False):
                self.extruderChanged = True
                i= 0
                for extruder in self._printer.get_tools():
                    svg_file = "styles/z-bolt/images/active.svg"
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(svg_file, self._gtk.content_width * .05 , self._gtk.content_height * .05)

                    self.extruders[i]['RadioButton'].set_from_pixbuf(pixbuf)
                    if self.extruders[i]['Extrude'] == None:
                     self.extruders[i]['EventBox'].connect("button-press-event", self.chanceExtruder, extruder)
                    self.extruders[i]['Extrude'] = extruder
                    if self.extruders[i]['Extrude'] != self.selectedExtruder:
                        self.extruders[i]['EventBox'].get_style_context().remove_class("extrude-active")

                    else:
                        self.extruders[i]['EventBox'].get_style_context().add_class("extrude-active")
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
                else:
                     self.extruder.updateValue(1/1, str(round(extruder_temp,1)) + f"° / {self.extruder_temp_target_pre}°")



            if(self.temp_heater_bed_temp != heater_bed_temp):
                self.temp_heater_bed_temp = heater_bed_temp
                if(self.heater_bed_temp_target_pre != 0):
                    self.heatedBed.updateValue(heater_bed_temp/self.heater_bed_temp_target_pre, str(round(heater_bed_temp,1)) + f"° / {self.heater_bed_temp_target_pre}°")
                else:
                    self.heatedBed.updateValue(1/1, str(round(heater_bed_temp,1)) + f"° / {self.heater_bed_temp_target_pre}°")

