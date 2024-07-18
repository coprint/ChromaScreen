import logging
import os
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintPrintingScreen(*args)


# class CoPrintPrintingScreen(ScreenPanel):

class Panel(ScreenPanel):     
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
       
        pageBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        pageBox.set_hexpand(True)


        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        self.continueButton.set_margin_left(self._gtk.action_bar_width *4)
        self.continueButton.set_margin_right(self._gtk.action_bar_width*4)
        image = self._gtk.Image("usb-wait", self._gtk.content_width * .25 , self._gtk.content_height * .25)
        self.continueButton.set_always_show_image (True)
        self.continueButton.set_image(image)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.pack_start(self.continueButton, False, True, 0)
        buttonBox.set_center_widget(self.continueButton)


        menu1 = Gtk.Label(("Dashboard"))
        menu2 = Gtk.Label(("Print Files"))
        menu3 = Gtk.Label(("Printers"))
        menu4= Gtk.Label(("Configure"))
        menuBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        menuBox.pack_start(buttonBox, True, True, 0)
        menuBox.pack_end(menu2, True, True, 0)
        menuBox.pack_end(menu3, True, True, 0)
        menuBox.pack_end(menu4, True, True, 0)
        
        #main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        #main.pack_start(pageBox, True, True, 0)
        #main.pack_end(menuBox, False, True, 50)
       
      


        #denemee
        self.start_timer()
      
        self.label1 = Gtk.Label("Dashboard")
        self.label2 = Gtk.Label("Dashboard")
        self.label3 = Gtk.Label("Dashboard")
        self.label4 = Gtk.Label("Dashboard")
        self.label5 = Gtk.Label("Dashboard")
        self.label6 = Gtk.Label("Dashboard")
        self.label7 = Gtk.Label("Dashboard")
        self.label8 = Gtk.Label("Dashboard")
        self.label9 = Gtk.Label("Dashboard")
        labelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        labelBox.pack_start(self.label1, True, True, 0)
        labelBox.pack_start(self.label3, True, True, 0)
        labelBox.pack_start(self.label4, True, True, 0)
        labelBox.pack_start(self.label5, True, True, 0)
        labelBox.pack_start(self.label6, True, True, 0)
        labelBox.pack_start(self.label7, True, True, 0)
        labelBox.pack_start(self.label8, True, True, 0)
        labelBox.pack_start(self.label9, True, True, 0)
        labelBox.pack_end(self.label2, True, True, 0)


        self.content.add(labelBox)
        self._screen.base_panel.visible_menu(False)
       
    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate
    
    def start_timer(self):
        """ Start the timer. """
        self.timeout_id = GLib.timeout_add(1500, self.on_timeout, None)
        

    def on_timeout(self, *args, **kwargs):
        heater_bed_temp = 0
        heater_bed_array = self._printer.get_temp_store('heater_bed')
        heater_bed_temp = heater_bed_array['temperatures'][-1]
        self.label1.set_text('Heater Bed: ' + str(heater_bed_temp))
        
        extruder_temp = 0
        extruder_array = self._printer.get_temp_store('extruder')
        extruder_temp = extruder_array['temperatures'][-1]
        self.label2.set_text('Extruder Bed: ' + str(extruder_temp))
        
        data = self._printer.data
        speed_factor = data['gcode_move']['speed_factor'] * 100
        extrude_factor = data['gcode_move']['extrude_factor'] * 100

        machine_velocity = data['toolhead']['max_velocity']
        square_corner_velocity = data['toolhead']['square_corner_velocity']
        max_accel = data['toolhead']['max_accel']
        max_accel_to_decel = data['toolhead']['max_accel_to_decel']
        fan_spped = data['fan']['speed']  *100

       
        self.label3.set_text('Speed Factor: ' + str(int(speed_factor)))
        self.label5.set_text('Extrude Factor: ' + str(int(extrude_factor)))
        self.label4.set_text('Fan Speed: ' + str(int(fan_spped)))
        self.label6.set_text('machine_velocity: ' + str(int(machine_velocity)))
        self.label7.set_text('max_accel: ' + str(int(max_accel)))
        self.label8.set_text('square_corner_velocity: ' + str(int(square_corner_velocity)))
        self.label9.set_text('max_accel_to_decel: ' + str(int(max_accel_to_decel)))

        return True
    
    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_printing_selection", "co_print_printing_selection", None, 1, True)
        
   
