import logging
import os

from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.addnetworkdialog import AddNetworkDialog
from ks_includes.widgets.infodialog import InfoDialog
from ks_includes.widgets.wificard import WifiCard

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintInputShaperScreen(*args)


# class CoPrintInputShaperScreen(ScreenPanel):
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

        self.menu = BottomMenu(self, False)
        self.inputShaperTye = ""
        printerTypeLabel = Gtk.Label(_("Select Your Printer Type"), name="printer-type-title-label")
        printerTypeLabel.set_justify(Gtk.Justification.CENTER)
        self.printerTypeLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.printerTypeLabelBox.set_halign(Gtk.Align.CENTER)
        self.printerTypeLabelBox.pack_start(printerTypeLabel, False, False, 0)

        printerTypeContentLabel = Gtk.Label(
            _("Calibration steps vary depending on your printer's motion mechanism. Please select the type of your printer."),
            name="printer-type-content-label")
        printerTypeContentLabel.set_max_width_chars(60)
        printerTypeContentLabel.set_line_wrap(True)
        printerTypeContentLabel.set_justify(Gtk.Justification.CENTER)
        self.printerTypeContentLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.printerTypeContentLabelBox.set_halign(Gtk.Align.CENTER)
        self.printerTypeContentLabelBox.pack_start(printerTypeContentLabel, False, False, 0)

        self.InputShaperLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.InputShaperLabelBox.set_valign(Gtk.Align.CENTER)
        self.InputShaperLabelBox.set_halign(Gtk.Align.CENTER)
        self.InputShaperLabelBox.set_hexpand(True)
        self.InputShaperLabelBox.pack_start(self.printerTypeLabelBox, False, False, 0)
        self.InputShaperLabelBox.pack_end(self.printerTypeContentLabelBox, False, False, 10)

        cartesianTypeImage = self._gtk.Image("printer", self._screen.width * .25, self._screen.width * .25)
        cartesianTypeLabel = Gtk.Label(_("Cartesian Type"), name="printer-type-label")
        cartesianTypeBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        cartesianTypeBox.set_halign(Gtk.Align.CENTER)
        cartesianTypeBox.set_name("printer-type-box")
        cartesianTypeBox.pack_start(cartesianTypeImage, False, False, 0)
        cartesianTypeBox.pack_start(cartesianTypeLabel, False, False, 0)

        cartesianTypeEventBox = Gtk.EventBox()
        cartesianTypeEventBox.connect("button-press-event", self.on_printer_box_clicked, "cartesianType")
        cartesianTypeEventBox.add(cartesianTypeBox)

        corexyTypeImage = self._gtk.Image("corexyPrinter", self._screen.width * .25, self._screen.width * .25)
        corexyTypeLabel = Gtk.Label(_("Corexy Type"), name="printer-type-label")
        corexyTypeBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        corexyTypeBox.set_halign(Gtk.Align.CENTER)
        corexyTypeBox.set_name("printer-type-box")
        corexyTypeBox.pack_start(corexyTypeImage, False, False, 0)
        corexyTypeBox.pack_start(corexyTypeLabel, False, False, 0)

        corexyTypeEventBox = Gtk.EventBox()
        corexyTypeEventBox.connect("button-press-event", self.on_printer_box_clicked, "corexyType")
        corexyTypeEventBox.add(corexyTypeBox)

        self.printersBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        self.printersBox.set_halign(Gtk.Align.CENTER)
        self.printersBox.pack_start(cartesianTypeEventBox, False, False, 0)
        self.printersBox.pack_end(corexyTypeEventBox, False, False, 0)

        self.main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main.set_vexpand(True)
        self.main.set_hexpand(True)
        self.main.set_halign(Gtk.Align.CENTER)
        self.main.pack_start(self.printersBox, False, False, 0)

        self.page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.page.set_vexpand(True)
        self.page.pack_start(self.InputShaperLabelBox, False, False, 0)
        self.page.pack_start(self.main, True, True, 0)
        self.page.pack_end(self.menu, False, True, 0)

        self.content.add(self.page)

    def on_printer_box_clicked(self, widget, event, inputShaperTye):

        self.inputShaperTye = inputShaperTye
        for child in self.printerTypeLabelBox.get_children():
            self.printerTypeLabelBox.remove(child)

        printerTypeLabel = Gtk.Label(_("Connect the Sensor"), name="printer-type-title-label")
        printerTypeLabel.set_justify(Gtk.Justification.CENTER)
        self.printerTypeLabelBox.set_halign(Gtk.Align.CENTER)
        self.printerTypeLabelBox.pack_start(printerTypeLabel, False, False, 0)

        for child in self.printerTypeContentLabelBox.get_children():
            self.printerTypeContentLabelBox.remove(child)

        printerTypeContentLabel = Gtk.Label(_("Place the Initial Sensor to the head of your printer."),
                                            name="printer-type-content-label")
        printerTypeContentLabel.set_max_width_chars(60)
        printerTypeContentLabel.set_line_wrap(True)
        printerTypeContentLabel.set_justify(Gtk.Justification.CENTER)
        self.printerTypeContentLabelBox.set_halign(Gtk.Align.CENTER)
        self.printerTypeContentLabelBox.pack_start(printerTypeContentLabel, False, False, 0)

        for child in self.printersBox.get_children():
            self.printersBox.remove(child)

        sensorImage = self._gtk.Image("sensor", self._screen.width * .5, self._screen.width * .5)
        sensorLabel = Gtk.Label(
            _("Calibration will disconnect from other printers. Please make sure that other printers are not in operation"),
            name="sensor-label")
        sensorLabel.set_max_width_chars(45)
        sensorLabel.set_line_wrap(True)
        sensorLabel.set_justify(Gtk.Justification.CENTER)

        nextStepButton = Gtk.Button(_('Next Step'), name="next-step-button")
        nextStepButton.connect("clicked", self.check_sensor_connection_page)
        nextStepButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        nextStepButtonBox.set_halign(Gtk.Align.CENTER)
        nextStepButtonBox.pack_start(nextStepButton, False, False, 0)

        sensorBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        sensorBox.set_valign(Gtk.Align.CENTER)
        sensorBox.pack_start(sensorImage, False, False, 0)
        sensorBox.pack_start(sensorLabel, False, False, 0)
        sensorBox.pack_start(nextStepButtonBox, False, False, 0)

        self.printersBox.pack_start(sensorBox, False, False, 0)

        self.content.show_all()

    def process_update(self, action, data):
        # if self._printer.state == 'error' or self._printer.state == 'shutdown' or self._printer.state ==  'disconnected':
        #     page_url = 'co_print_home_not_connected_screen'
        #     self._screen.show_panel(page_url, page_url, "Language", 1, False)    

        if action == "notify_gcode_response":
            if data.startswith('//') and data.endswith('"ACCELEROMETER_QUERY"'):
                self.sensor_cannot_connected_page(None, 1)
            if data.startswith('!!') and 'Invalid' in data :
                self.sensor_cannot_connected_page(None, 2)
            if data.startswith('//') and 'accelerometer values' in data :
                self.sensor_connected_page(None)

    def finished_sensor_check(self, result, method, params):
        print(result)
        if result['result'] == 'ok':
            self.sensor_connected_page(None)

    def check_sensor_connection_page(self, widget):

        for child in self.page.get_children():
            self.page.remove(child)

        spinner = Gtk.Spinner()
        spinner.props.width_request = 100
        spinner.props.height_request = 100
        spinner.start()

        titleLabel = Gtk.Label(_("Checking the Sensor Connection"), name="printer-type-title-label")
        contentLabel = Gtk.Label(_("Please Wait"), name="printer-type-content-label")

        passiveNextStepButton = Gtk.Button(_('Next Step'), name="passive-next-step-button")
        passiveNextStepButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        passiveNextStepButtonBox.set_halign(Gtk.Align.CENTER)
        passiveNextStepButtonBox.pack_start(passiveNextStepButton, False, False, 0)

        checkingSensorConnectionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        checkingSensorConnectionBox.set_halign(Gtk.Align.CENTER)
        checkingSensorConnectionBox.pack_start(spinner, False, False, 50)
        checkingSensorConnectionBox.pack_start(titleLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(contentLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(passiveNextStepButtonBox, False, False, 50)

        self.page.pack_start(checkingSensorConnectionBox, True, True, 0)
        self.page.pack_end(self.menu, False, True, 0)
        # self.start_timer_sensor_connection_page()
        self._screen._ws.klippy.gcode_script("ACCELEROMETER_QUERY")
        self.content.show_all()

    def start_timer_sensor_connection_page(self):
        """ Start the timer. """
        self.sensor_timeout_id = GLib.timeout_add(4000, self.sensor_connected_page, None)

    def start_timer_xaxis_progress_page(self):
        """ Start the timer. """
        self.xaxis_timeout_id = GLib.timeout_add(4000, self.xaxis_complete_page, None)

    def start_timer_yaxis_progress_page(self):
        """ Start the timer. """
        self.xaxis_timeout_id = GLib.timeout_add(4000, self.yaxis_complete_page, None)

    def sensor_connected_page(self, widget):
        self.sensor_timeout_id = None
        for child in self.page.get_children():
            self.page.remove(child)

        checkmark = self._gtk.Image("Checkmark", self._screen.width * .1, self._screen.width * .1)

        titleLabel = Gtk.Label(_("Sensor Connected"), name="printer-type-title-label")
        contentLabel = Gtk.Label(_("You are ready to start the test."), name="printer-type-content-label")

        nextStepButton = Gtk.Button(_('Start Calibration'), name="next-step-button")
        nextStepButton.connect("clicked", self.xaxis_progress_page)
        nextStepButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        nextStepButtonBox.set_halign(Gtk.Align.CENTER)
        nextStepButtonBox.pack_start(nextStepButton, False, False, 0)

        checkingSensorConnectionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        checkingSensorConnectionBox.set_halign(Gtk.Align.CENTER)
        checkingSensorConnectionBox.pack_start(checkmark, False, False, 50)
        checkingSensorConnectionBox.pack_start(titleLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(contentLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(nextStepButtonBox, False, False, 50)

        self.page.pack_start(checkingSensorConnectionBox, True, True, 0)
        self.page.pack_end(self.menu, False, True, 0)

        self.content.show_all()
        return False

    def sensor_cannot_connected_page(self, widget, pop):
        logging.info(f"sensor cannot connected page")
        #self.sensor_timeout_id = None
        for child in self.page.get_children():
            self.page.remove(child)
        checkmark = self._gtk.Image("Cannotmark", self._screen.width * .1, self._screen.width * .1)
        titleLabel = Gtk.Label(_("Sensor Cannot Connect"), name="printer-type-title-label")
        message = (_("You aren't ready to start the test.\n Please connect your sensor or re-config your Input Shaper.\n Then try again."))
        if pop == 1:
            message = (_("You aren't ready to start the test.\n Please config your Input Shaper.\n Then try again."))
        elif pop == 2:
            message = (_("You aren't ready to start the test.\n Please re-config your Input Shaper.\n Then try again."))
        contentLabel = Gtk.Label(message, name="printer-type-content-label")
        contentLabel.set_max_width_chars(60)
        contentLabel.set_line_wrap(True)
        contentLabel.set_justify(Gtk.Justification.CENTER)
        nextStepButton = Gtk.Button(_('Check Sensor'), name="next-step-button")
        nextStepButton.connect("clicked", self.check_sensor_connection_page)
        nextStepButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        nextStepButtonBox.set_halign(Gtk.Align.CENTER)
        nextStepButtonBox.pack_start(nextStepButton, False, False, 0)

        checkingSensorConnectionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        checkingSensorConnectionBox.set_halign(Gtk.Align.CENTER)
        checkingSensorConnectionBox.pack_start(checkmark, False, False, 50)
        checkingSensorConnectionBox.pack_start(titleLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(contentLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(nextStepButtonBox, False, False, 50)

        self.page.pack_start(checkingSensorConnectionBox, True, True, 0)
        self.page.pack_end(self.menu, False, True, 0)

        self.content.show_all()
        return False

    def start_calibration_result(self, result, method, params):
        print(result)
        if result['result'] == 'ok':
            self.xaxis_complete_page(None)

    def finished_home(self, asd, a, b):
        self.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.destroy()
        self._screen._ws.klippy.gcode_script(self.get_gcode_script_for_start_calibration(), self.start_calibration_result)
    def home(self):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.HOME, self.finished_home)
        self.dialog = InfoDialog(self, _("Printer is returning to the starting position, please wait.."), False)
        self.dialog.get_style_context().add_class("alert-info-dialog")

        self.dialog.set_decorated(False)
        self.dialog.set_size_request(0, 0)
        # timer_duration = 1000
        # GLib.timeout_add(timer_duration, self.close_dialog, self.dialog)
        response = self.dialog.run()
    def xaxis_progress_page(self, widget):


        for child in self.page.get_children():
            self.page.remove(child)

        spinner = Gtk.Spinner()
        spinner.props.width_request = 100
        spinner.props.height_request = 100
        spinner.start()

        start_label = "X"
        if self.inputShaperTye == "corexyType":
            start_label = "XY"
        titleLabel = Gtk.Label(_(start_label + " Axis Vibration Detection in Progress"), name="printer-type-title-label")
        contentLabel = Gtk.Label(_("Please don’t touch the printer"), name="printer-type-content-label")

        passiveNextStepButton = Gtk.Button(_('Next Step'), name="passive-next-step-button")
        passiveNextStepButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        passiveNextStepButtonBox.set_halign(Gtk.Align.CENTER)
        passiveNextStepButtonBox.pack_start(passiveNextStepButton, False, False, 0)

        checkingSensorConnectionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        checkingSensorConnectionBox.set_halign(Gtk.Align.CENTER)
        checkingSensorConnectionBox.pack_start(spinner, False, False, 50)
        checkingSensorConnectionBox.pack_start(titleLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(contentLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(passiveNextStepButtonBox, False, False, 50)

        self.page.pack_start(checkingSensorConnectionBox, True, True, 0)
        self.page.pack_end(self.menu, False, True, 0)
       # self.start_timer_xaxis_progress_page()
        if self._printer.get_stat("toolhead", "homed_axes") != "xyz":
            self.home()
        else:
            self._screen._ws.klippy.gcode_script(self.get_gcode_script_for_start_calibration(), self.start_calibration_result)
        self.content.show_all()

    def get_gcode_script_for_start_calibration(self):
        if self.inputShaperTye == "cartesianType":
            return "SHAPER_CALIBRATE AXIS=X"
        else:
            return "SHAPER_CALIBRATE"
    def xaxis_complete_page(self, widget):
        self.xaxis_timeout_id = None
        for child in self.page.get_children():
            self.page.remove(child)

        checkmark = self._gtk.Image("Checkmark", self._screen.width * .1, self._screen.width * .1)

        start_label = "X"
        if self.inputShaperTye == "corexyType":
            start_label = "XY"

        titleLabel = Gtk.Label(_(start_label + " Axis Vibration Detection Complete"), name="printer-type-title-label")
        contentLabel = Gtk.Label(
            _(start_label + "-axis vibration compensation detection has been completed and the status is normal."),
            name="printer-type-content-label")
        self.startButton = ""
        if self.inputShaperTye == "corexyType":
            self.startButton = Gtk.Button(_('Complete'), name="next-step-button")
            self.startButton.connect("clicked", self.save_config)
        elif self.inputShaperTye == "cartesianType":
            self.startButton = Gtk.Button(_('Start Calibration'), name="next-step-button")
            self.startButton.connect("clicked", self.sensor_connection_pagee)
        startButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        startButtonBox.set_halign(Gtk.Align.CENTER)
        startButtonBox.pack_start(self.startButton, False, False, 0)

        checkingSensorConnectionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        checkingSensorConnectionBox.set_halign(Gtk.Align.CENTER)
        checkingSensorConnectionBox.pack_start(checkmark, False, False, 50)
        checkingSensorConnectionBox.pack_start(titleLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(contentLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(startButtonBox, False, False, 50)

        self.page.pack_start(checkingSensorConnectionBox, True, True, 0)
        self.page.pack_end(self.menu, False, True, 0)

        self.content.show_all()

        return False

    def sensor_connection_pagee(self, widget):

        for child in self.printerTypeLabelBox.get_children():
            self.printerTypeLabelBox.remove(child)

        printerTypeLabel = Gtk.Label(_("Please Connect the Sensor"), name="printer-type-title-label")
        printerTypeLabel.set_justify(Gtk.Justification.CENTER)
        self.printerTypeLabelBox.set_halign(Gtk.Align.CENTER)
        self.printerTypeLabelBox.pack_start(printerTypeLabel, False, False, 0)

        for child in self.printerTypeContentLabelBox.get_children():
            self.printerTypeContentLabelBox.remove(child)

        printerTypeContentLabel = Gtk.Label(
            _("Place the Initial Sensor on your printer's bed using double-sided tape."),
            name="printer-type-content-label")
        printerTypeContentLabel.set_max_width_chars(60)
        printerTypeContentLabel.set_line_wrap(True)
        printerTypeContentLabel.set_justify(Gtk.Justification.CENTER)
        self.printerTypeContentLabelBox.set_halign(Gtk.Align.CENTER)
        self.printerTypeContentLabelBox.pack_start(printerTypeContentLabel, False, False, 0)

        for child in self.printersBox.get_children():
            self.printersBox.remove(child)

        sensorImage = self._gtk.Image("tablapid", self._screen.width * .5, self._screen.width * .5)
        sensorLabel = Gtk.Label(_("Hot Bed"), name="printer-type-content-label")
        sensorLabel.set_max_width_chars(45)
        sensorLabel.set_line_wrap(True)
        sensorLabel.set_justify(Gtk.Justification.CENTER)

        nextStepButton = Gtk.Button(_('Start Calibration'), name="next-step-button")
        nextStepButton.connect("clicked", self.yaxis_progress_page)
        nextStepButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        nextStepButtonBox.set_halign(Gtk.Align.CENTER)
        nextStepButtonBox.pack_start(nextStepButton, False, False, 0)

        sensorBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        sensorBox.set_valign(Gtk.Align.CENTER)
        sensorBox.pack_start(sensorImage, False, False, 0)
        sensorBox.pack_start(sensorLabel, False, False, 0)
        sensorBox.pack_start(nextStepButtonBox, False, False, 20)

        self.printersBox.pack_start(sensorBox, False, False, 0)
        self.main.pack_start(self.printersBox, False, False, 0)

        for child in self.page.get_children():
            self.page.remove(child)

        self.page.pack_start(self.InputShaperLabelBox, False, False, 0)
        self.page.pack_start(self.main, True, True, 0)
        self.page.pack_end(self.menu, False, True, 0)

        self.content.show_all()

    def yaxis_progress_page(self, widget):
        for child in self.page.get_children():
            self.page.remove(child)

        spinner = Gtk.Spinner()
        spinner.props.width_request = 100
        spinner.props.height_request = 100
        spinner.start()

        titleLabel = Gtk.Label(_("Y Axis Vibration Detection in Progress"), name="printer-type-title-label")
        contentLabel = Gtk.Label(_("Please don’t touch the printer"), name="printer-type-content-label")

        passiveNextStepButton = Gtk.Button(_('Next Step'), name="passive-next-step-button")
        passiveNextStepButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        passiveNextStepButtonBox.set_halign(Gtk.Align.CENTER)
        passiveNextStepButtonBox.pack_start(passiveNextStepButton, False, False, 0)

        checkingSensorConnectionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        checkingSensorConnectionBox.set_halign(Gtk.Align.CENTER)
        checkingSensorConnectionBox.pack_start(spinner, False, False, 50)
        checkingSensorConnectionBox.pack_start(titleLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(contentLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(passiveNextStepButtonBox, False, False, 50)

        self.page.pack_start(checkingSensorConnectionBox, True, True, 0)
        self.page.pack_end(self.menu, False, True, 0)
        #self.start_timer_yaxis_progress_page()
        self._screen._ws.klippy.gcode_script("SHAPER_CALIBRATE AXIS=Y", self.finished_y_calibrate)

       # yaxis_complete_page
        self.content.show_all()
    def finished_y_calibrate(self, result, method, params):
        print(result)
        if result['result'] == 'ok':
            self.yaxis_complete_page(None)

    def save_config(self, widget):

        script = {"script": "SAVE_CONFIG"}
        self._screen._confirm_send_action(
            None,
            _("Save configuration?") + "\n\n" + _("Klipper will reboot"),
            "printer.gcode.script",
            script
        )
        self._screen.show_panel("co_print_home_screen", "co_print_home_screen", "Language", 1, False)

    def yaxis_complete_page(self, widget):
        self.xaxis_timeout_id = None
        for child in self.page.get_children():
            self.page.remove(child)

        checkmark = self._gtk.Image("Checkmark", self._screen.width * .1, self._screen.width * .1)

        titleLabel = Gtk.Label(_("Y Axis Vibration Detection Complete"), name="printer-type-title-label")
        contentLabel = Gtk.Label(
            _("Y-axis vibration compensation detection has been completed and the status is normal."),
            name="printer-type-content-label")

        self.startButton = Gtk.Button(_('Complete'), name="next-step-button")
        self.startButton.connect("clicked", self.save_config)
        startButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        startButtonBox.set_halign(Gtk.Align.CENTER)
        startButtonBox.pack_start(self.startButton, False, False, 0)

        checkingSensorConnectionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        checkingSensorConnectionBox.set_halign(Gtk.Align.CENTER)
        checkingSensorConnectionBox.pack_start(checkmark, False, False, 50)
        checkingSensorConnectionBox.pack_start(titleLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(contentLabel, False, False, 0)
        checkingSensorConnectionBox.pack_start(startButtonBox, False, False, 50)

        self.page.pack_start(checkingSensorConnectionBox, True, True, 0)
        self.page.pack_end(self.menu, False, True, 0)

        self.content.show_all()

        return False
