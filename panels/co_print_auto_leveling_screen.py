import logging
import os
from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.infodialog import InfoDialog


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintAutoLevelingScreen(*args)


# class CoPrintAutoLevelingScreen(ScreenPanel):
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

        menu = BottomMenu(self, False)

        self.grid = Gtk.Grid(column_homogeneous=True,
                             column_spacing=0,
                             row_spacing=0)
        self.count_grid = 0
        self.row_grid = 0
        row = 4
        row_s = 0
        count_s = 0
        count = 0
        calibration_value = " 0.00"
        self.numberlabel = {}
        self.numberLabelBox = {}
        direction = '+'
        self.z_cal_values = []

        for x in range(25):

            self.numberlabel[str(row_s) + '/' + str(count_s)] = Gtk.Label(calibration_value, name="auto-leveling-label")
            self.numberLabelBox[str(row_s) + '/' + str(count_s)] = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                                                           spacing=0)
            self.numberLabelBox[str(row_s) + '/' + str(count_s)].set_valign(Gtk.Align.CENTER)
            self.numberLabelBox[str(row_s) + '/' + str(count_s)].set_halign(Gtk.Align.CENTER)
            self.numberLabelBox[str(row_s) + '/' + str(count_s)].set_name("auto-leveling-label-box")
            self.numberLabelBox[str(row_s) + '/' + str(count_s)].add(self.numberlabel[str(row_s) + '/' + str(count_s)])

            self.grid.attach(self.numberLabelBox[str(row_s) + '/' + str(count_s)], count, row, 1, 1)



            if direction == '+':
                count += 1
            else:
                count -= 1
            count_s += 1
            if count == 5:
                count-=1
                direction = '-'
                count_s = 0
                row -= 1
                row_s += 1
            if count == -1:
                count += 1
                direction = '+'
                count_s = 0
                row -= 1
                row_s += 1


        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        left_box.pack_start(self.grid, False, False, 0)

        autoLevelingLabel = Gtk.Label(_("Automatic Table Calibration"), name="auto-leveling-title-label")
        autoLevelingContentLabel = Gtk.Label(
            _("Click the “Start Calibration” button to perform automatic table calibration."),
            name="auto-leveling-content-label")
        autoLevelingContentLabel.set_max_width_chars(35)
        autoLevelingContentLabel.set_line_wrap(True)
        autoLevelingContentLabel.set_justify(Gtk.Justification.CENTER)
        self.autoLevelingContentLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.autoLevelingContentLabelBox.pack_start(autoLevelingContentLabel, False, False, 0)

        autoLevelingBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        autoLevelingBox.pack_start(autoLevelingLabel, False, False, 0)
        autoLevelingBox.pack_start(self.autoLevelingContentLabelBox, False, False, 10)

        self.temperatureButton = Gtk.Button(_('Save'), name="probe-calibration-start-button")
        self.temperatureButton.connect("clicked", self.save_calibration)
        temperatureButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        temperatureButtonBox.set_halign(Gtk.Align.CENTER)
        temperatureButtonBox.pack_start(self.temperatureButton, False, False, 0)

        self.startButton = Gtk.Button(_('Start Calibration'), name="probe-calibration-start-button")
        self.startButton.connect("clicked", self.start_calibration)
        startButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        startButtonBox.set_halign(Gtk.Align.CENTER)
        startButtonBox.pack_start(self.startButton, False, False, 0)

        self.buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.buttonBox.set_halign(Gtk.Align.CENTER)
        self.buttonBox.set_name("probe-calibration-start-button-box")
        self.buttonBox.pack_start(startButtonBox, True, False, 0)
        self.buttonBox.pack_start(temperatureButtonBox, True, False, 0)

        self.spinnerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.spinnerBox.set_halign(Gtk.Align.CENTER)
        self.spinnerBox.set_valign(Gtk.Align.CENTER)

        self.right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.right_box.set_name("auto-leveling-right-box")
        self.right_box.pack_start(autoLevelingBox, False, False, 20)
        self.right_box.pack_start(self.spinnerBox, False, False, 20)
        self.right_box.pack_end(self.buttonBox, False, False, 70)

        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        main_box.set_vexpand(True)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.pack_start(left_box, False, True, 0)
        main_box.pack_start(self.right_box, False, False, 0)

        self.page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)

        self.page.pack_start(main_box, False, True, 0)
        self.page.pack_end(menu, False, True, 0)


        self.content.add(self.page)

    def process_update(self, action, data):
        # if self._printer.state == 'error' or self._printer.state == 'shutdown' or self._printer.state ==  'disconnected':
        #     page_url = 'co_print_home_not_connected_screen'
        #     self._screen.show_panel(page_url, page_url, "Language", 1, False)    
        if action == "notify_status_update":
             if ('configfile' in data) and data['configfile']['save_config_pending_items']['bed_mesh default']['points']:
                 matrix_array= []
                 pending_data = data['configfile']['save_config_pending_items']['bed_mesh default']['points']
                 pending_data.split('\n')
                 for index_x, x in enumerate( pending_data.split('\n ')):
                      if x != '':
                        array_x = x.split(', ')
                        for index_y, value_s in enumerate(array_x):
                                if value_s != '':
                                    value = "{:.2f}".format( float(value_s))
                                    self.numberlabel[str(index_x-1) + '/' + str(index_y)].set_label(str(value))
                                    
                                    self.numberLabelBox[str(index_x-1) + '/' + str(index_y)].get_style_context().remove_class(
                                        "auto-leveling-label-box-active-white")
                                    self.numberLabelBox[str(index_x-1) + '/' + str(index_y)].get_style_context().add_class(
                                        "auto-leveling-label-box-active")

             if 'bed_mesh' in data:
                matrix_array= []
                if len(data['bed_mesh']['probed_matrix']) > 1:
                    matrix_array = data['bed_mesh']['probed_matrix']
                   
                    print(data['bed_mesh']['probed_matrix'])
                else:
                     if 'default' in data['bed_mesh']['profiles']:
                         matrix_array = data['bed_mesh']['profiles']['default']['points']
                for index_x, x in enumerate(matrix_array):
                        for index_y, value in enumerate(x):
                            self.numberlabel[str(index_x) + '/' + str(index_y)].set_label(str(value))
                            
                            self.numberLabelBox[str(index_x) + '/' + str(index_y)].get_style_context().remove_class(
                                "auto-leveling-label-box-active-white")
                            self.numberLabelBox[str(index_x) + '/' + str(index_y)].get_style_context().add_class(
                                "auto-leveling-label-box-active")
                            #if index_x < 5:
                            # self.numberLabelBox[str(index_x) + '/' + str(index_y)].get_style_context().add_class(
                            #   "auto-leveling-label-box-active-white")

        if action == "notify_gcode_response":
            # print(data)
            if data.find("z=") != -1:
               # if len(self.z_cal_values) <  25:
                    xy = data.split(" ")[3].split(',')
                    val = {"x" : xy[0], "y": xy[1],  "z": data.split("z=", 1)[1]}
                    print(data.split("z=", 1)[1])
                    calibration_value = str(round(float(data.split("z=", 1)[1]), 2))
                    #self.numberlabel[str(self.row_grid) + '/' + str(self.count_grid)].set_label(calibration_value)
                    
                    #self.numberLabelBox[str(self.row_grid) + '/' + str(self.count_grid)].get_style_context().remove_class(
                    #    "auto-leveling-label-box-active-white")
                    #self.numberLabelBox[str(self.row_grid) + '/' + str(self.count_grid)].get_style_context().add_class(
                    #    "auto-leveling-label-box-active")
                    self.z_cal_values.append(val)
                    print(len(self.z_cal_values))

                    self.count_grid += 1
                    if self.count_grid % 5 == 0:
                        self.count_grid = 0
                        self.row_grid += 1
                   # if self.row_grid < 5:
                     #   self.numberLabelBox[str(self.row_grid) + '/' + str(self.count_grid)].get_style_context().add_class(
                      #      "auto-leveling-label-box-active-white")

        # if self._printer.state != 'error':

        # print(self._printer.data['bed_mesh']['probed_matrix'])
    def save_calibration(self, widget):
         self.save_config()
    def start_calibration(self, widget):
        self.count_grid = 0
        self.row_grid = 0
        for x in range(25):
            self.numberlabel[str(self.row_grid) + '/' + str(self.count_grid)].set_label(" 0.00")
            self.numberLabelBox[str(self.row_grid) + '/' + str(self.count_grid)].get_style_context().remove_class(
                "auto-leveling-label-box-active-white")
            self.numberLabelBox[str(self.row_grid) + '/' + str(self.count_grid)].get_style_context().remove_class(
                "auto-leveling-label-box-active")
            self.count_grid += 1
            if self.count_grid % 5 == 0:
                self.count_grid = 0
                self.row_grid += 1

        self.count_grid = 0
        self.row_grid = 0
    
        self.z_cal_values = []
        self.spinner = Gtk.Spinner()
        self.spinner.props.width_request = 70
        self.spinner.props.height_request = 70
        self.spinner.start()

        for child in self.spinnerBox.get_children():
            self.spinnerBox.remove(child)

        self.spinnerBox.add(self.spinner)

        for child in self.autoLevelingContentLabelBox.get_children():
            self.autoLevelingContentLabelBox.remove(child)

        autoLevelingContentLabel = Gtk.Label(_("Automatic bed leveling is being performed. Please wait.."),
                                             name="auto-leveling-content-label")
        autoLevelingContentLabel.set_max_width_chars(25)
        autoLevelingContentLabel.set_line_wrap(True)
        autoLevelingContentLabel.set_justify(Gtk.Justification.CENTER)
        self.autoLevelingContentLabelBox.pack_start(autoLevelingContentLabel, False, False, 0)

        for child in self.buttonBox.get_children():
            self.buttonBox.remove(child)

        stopButton = Gtk.Button(_('Stop Calibrating'), name="calibration-stop-button")
        stopButton.connect("clicked", self.stop_calibration)
        stopButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        stopButtonBox.set_halign(Gtk.Align.CENTER)
        stopButtonBox.pack_start(stopButton, False, False, 0)
        # self.buttonBox.pack_start(stopButtonBox, True, False, 0)

        self.content.show_all()
        self.calibrate_mesh()
        return True

    def stop_calibration(self, widget):
        self.count_grid = 0
        self.row_grid = 0
        for x in range(25):
            self.numberlabel[str(self.row_grid) + '/' + str(self.count_grid)].set_label(" 0.00")
            self.numberLabelBox[str(self.row_grid) + '/' + str(self.count_grid)].get_style_context().remove_class(
                "auto-leveling-label-box-active-white")
            self.numberLabelBox[str(self.row_grid) + '/' + str(self.count_grid)].get_style_context().remove_class(
                "auto-leveling-label-box-active")
            self.count_grid += 1
            if self.count_grid % 5 == 0:
                self.count_grid = 0
                self.row_grid += 1

        self.count_grid = 0
        self.row_grid = 0

        for child in self.spinnerBox.get_children():
            self.spinnerBox.remove(child)

        for child in self.autoLevelingContentLabelBox.get_children():
            self.autoLevelingContentLabelBox.remove(child)

        autoLevelingContentLabel = Gtk.Label(
            _("Click the “Start Calibration” button to perform automatic table calibration."),
            name="auto-leveling-content-label")
        autoLevelingContentLabel.set_max_width_chars(35)
        autoLevelingContentLabel.set_line_wrap(True)
        autoLevelingContentLabel.set_justify(Gtk.Justification.CENTER)
        self.autoLevelingContentLabelBox.pack_start(autoLevelingContentLabel, False, False, 0)

        for child in self.buttonBox.get_children():
            self.buttonBox.remove(child)

        self.temperatureButton = Gtk.Button(_('Save'), name="probe-calibration-start-button")
        self.temperatureButton.connect("clicked", self.save_calibration)
        temperatureButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        temperatureButtonBox.set_halign(Gtk.Align.CENTER)
        temperatureButtonBox.pack_start(self.temperatureButton, False, False, 0)

        self.startButton = Gtk.Button(_('Start Calibration'), name="probe-calibration-start-button")
        self.startButton.connect("clicked", self.start_calibration)
        startButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        startButtonBox.set_halign(Gtk.Align.CENTER)
        startButtonBox.pack_start(self.startButton, False, False, 0)

        self.buttonBox.pack_start(startButtonBox, True, False, 0)
        self.buttonBox.pack_start(temperatureButtonBox, True, False, 0)

        self.content.show_all()
        return True

    def home(self):
        self._screen._ws.klippy.gcode_script(KlippyGcodes.HOME, self.finished)
        self.dialog = InfoDialog(self, _("Printer is returning to the starting position, please wait.."), False)
        self.dialog.get_style_context().add_class("alert-info-dialog")

        self.dialog.set_decorated(False)
        self.dialog.set_size_request(0, 0)
        # timer_duration = 1000
        # GLib.timeout_add(timer_duration, self.close_dialog, self.dialog)
        response = self.dialog.run()

    def finished(self, asd, a, b):
        self.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.destroy()
        self._screen._ws.send_method("printer.gcode.script", {"script": "BED_MESH_CALIBRATE"}, self.finished_calibrate)
        # self._screen._ws.klippy.gcode_script("BED_MESH_CALIBRATE")

    def finished_calibrate(self, result, method, params):
        print(result)
       
        self.stop_calibration(None)
       
        if  ('error' in result) == False:
            #self.save_config()
            print('success')
        else:
            self.open_info_dialog(str(result['error']))
        # self._screen._ws.klippy.gcode_script("SAVE_CONFIG")


    def open_info_dialog(self, error):
        self.dialog = InfoDialog(self, (error), True)
        self.dialog.get_style_context().add_class("alert-info-dialog")
       
        self.dialog.set_decorated(False)
        self.dialog.set_size_request(0, 0)
      
     

        response = self.dialog.run()
 

    def save_config(self):

        script = {"script": "SAVE_CONFIG"}
        self._screen._confirm_send_action(
            None,
            _("Save configuration?") + "\n\n" + _("Klipper will reboot"),
            "printer.gcode.script",
            script
        )

    def calibrate_mesh(self):
        #self.stop_calibration(None)
        self._screen.show_popup_message(_("Calibrating"), level=1)
        if self._printer.get_stat("toolhead", "homed_axes") != "xyz":
            self.home()
        else:
            self._screen._ws.send_method("printer.gcode.script", {"script": "BED_MESH_CALIBRATE"},
                                         self.finished_calibrate)

    def start_timer(self):
        """ Start the timer. """
        self.timeout_id = GLib.timeout_add(5000, self.on_timeout, None)

    def send_save_mesh(self, widget):
        self._screen._ws.klippy.gcode_script("BED_MESH_CALIBRATE")

    def on_timeout(self, *args, **kwargs):
        for child in self.spinnerBox.get_children():
            self.spinnerBox.remove(child)

        checkmark = self._gtk.Image("Checkmark", self._screen.width * .09, self._screen.width * .09)
        self.spinnerBox.add(checkmark)

        for child in self.autoLevelingContentLabelBox.get_children():
            self.autoLevelingContentLabelBox.remove(child)

        autoLevelingContentLabel = Gtk.Label(_("Automatic bed calibration is completed. Please restart the system."),
                                             name="auto-leveling-content-label")
        autoLevelingContentLabel.set_max_width_chars(35)
        autoLevelingContentLabel.set_line_wrap(True)
        autoLevelingContentLabel.set_justify(Gtk.Justification.CENTER)
        self.autoLevelingContentLabelBox.pack_start(autoLevelingContentLabel, False, False, 0)

        for child in self.buttonBox.get_children():
            self.buttonBox.remove(child)

        rebootButton = Gtk.Button(_('Save MESH'), name="probe-calibration-start-button")
        rebootButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.startButton.connect("clicked", self.send_save_mesh)
        rebootButtonBox.set_halign(Gtk.Align.CENTER)
        rebootButtonBox.pack_start(rebootButton, False, False, 0)

        self.buttonBox.pack_start(rebootButtonBox, True, False, 0)

        self.content.show_all()

        self.timeout_id = None

        return False
