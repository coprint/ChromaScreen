import logging
import os
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.keypad_new import KeyPadNew
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintMovementSettingScreen(*args)



class CoPrintMovementSettingScreen(ScreenPanel):

    
    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        menu = BottomMenu(self, False)
        conf = self._printer.get_config_section("printer")
        #Acceleration#
        accelerationLabel = Gtk.Label(_("Acceleration"))
        accelerationLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        accelerationLabelBox.set_name("movement-name-box")
        accelerationLabelBox.pack_start(accelerationLabel, False, False, 0)
        
        self.accelerationnumberLabel = Gtk.Label("0", name="movement-label")

        self.scaleAcceleration = Gtk.Scale()
        self.scaleAcceleration.set_range(0, int(conf['max_accel']))
        self.scaleAcceleration.set_value(0)
        self.scaleAcceleration.set_increments(1, 1)
        self.scaleAcceleration.set_digits(1)
        self.scaleAcceleration.set_draw_value(False)
        self.scaleAcceleration.set_hexpand(True)
        self.scaleAcceleration.connect("value-changed", self.on_scale_changed, self.accelerationnumberLabel, "SET_VELOCITY_LIMIT ACCEL=")
        scaleStyle = self.scaleAcceleration.get_style_context()
        scaleStyle.add_class("movement-setting")
        unitLabel = Gtk.Label(_("mm/s"))   
        
        accelerationnumberBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        accelerationnumberBox.set_valign(Gtk.Align.CENTER)
        accelerationnumberBox.set_halign(Gtk.Align.CENTER)
        accelerationnumberBox.set_name("movement-label-box")
        accelerationnumberBox.add(self.accelerationnumberLabel)
        
        
        AccelerationBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        AccelerationBox.set_name("movement-settings-box")
        AccelerationBox.pack_start(accelerationLabelBox, False, False, 0)
        AccelerationBox.pack_end(unitLabel, False, True, 0)
        AccelerationBox.pack_end(accelerationnumberBox, False, False, 0)
        AccelerationBox.pack_end(self.scaleAcceleration, False, True, 30)
        
        #Accel to Decel#
        DecelLabel = Gtk.Label(_("Accel to Decel"))
        decelLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        decelLabelBox.set_name("movement-name-box")
        decelLabelBox.pack_start(DecelLabel, False, False, 0)
        self.decelnumberLabel = Gtk.Label("0", name="movement-label")
        self.scaleDecel = Gtk.Scale()
        self.scaleDecel.set_range(0, int(conf['max_accel']))
        self.scaleDecel.set_value(0)
        self.scaleDecel.set_increments(1, 1)
        self.scaleDecel.set_digits(1)
        self.scaleDecel.set_draw_value(False)
        self.scaleDecel.set_hexpand(True)
        self.scaleDecel.connect("value-changed", self.on_scale_changed, self.decelnumberLabel, "SET_VELOCITY_LIMIT ACCEL_TO_DECEL=")
        scaleStyle = self.scaleDecel.get_style_context()
        scaleStyle.add_class("movement-setting")
        unitLabel2 = Gtk.Label(_("mm/s"))   
        
        decelnumberLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        decelnumberLabelBox.set_valign(Gtk.Align.CENTER)
        decelnumberLabelBox.set_halign(Gtk.Align.CENTER)
        decelnumberLabelBox.set_name("movement-label-box")
        decelnumberLabelBox.add(self.decelnumberLabel)
        
        
        DecelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        DecelBox.set_name("movement-settings-box")
        DecelBox.pack_start(decelLabelBox, False, False, 0)
        DecelBox.pack_end(unitLabel2, False, True, 0)
        DecelBox.pack_end(decelnumberLabelBox, False, False, 0)
        DecelBox.pack_end(self.scaleDecel, False, True, 30)
        
        #Velocity
        velocityLabel = Gtk.Label(_("Velocity"))
        velocityLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        velocityLabelBox.set_name("movement-name-box")
        velocityLabelBox.pack_start(velocityLabel, False, False, 0)
        self.velocityNumberLabel = Gtk.Label("0", name="movement-label")
        velocitynumPadIcon = self._gtk.Image("calculator", self._screen.width *.03, self._screen.width *.03)
        velocitynumPadButton = Gtk.Button(name ="speed-factor-button")
        velocitynumPadButton.connect("clicked", self.open_numpad, self.velocityNumberLabel, "SET_VELOCITY_LIMIT VELOCITY=")
        velocitynumPadButton.set_image(velocitynumPadIcon)
        velocitynumPadButton.set_always_show_image(True)
        
        unitLabel3 = Gtk.Label(_("mm/s"))   
       
        velocityNumberLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        velocityNumberLabelBox.set_valign(Gtk.Align.CENTER)
        velocityNumberLabelBox.set_halign(Gtk.Align.CENTER)
        velocityNumberLabelBox.set_name("square-movement-label-box")
        velocityNumberLabelBox.pack_end(velocitynumPadButton, False, False, 0)
        velocityNumberLabelBox.pack_end(self.velocityNumberLabel, False, False, 0)
        
        velocityBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        velocityBox.set_name("movement-settings-box")
        velocityBox.pack_start(velocityLabelBox, False, False, 0)
        velocityBox.pack_end(unitLabel3, False, True, 0)
        velocityBox.pack_end(velocityNumberLabelBox, False, False, 0)
        
        #Square Corner Velocity
        squareCornerLabel = Gtk.Label(_("Square Corner Velocity"))
        squareCornerLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        squareCornerLabelBox.set_name("movement-name-box")
        squareCornerLabelBox.pack_start(squareCornerLabel, False, False, 0)
        self.squareCornerNumberLabel = Gtk.Label("0", name="movement-label")
        squarenumPadIcon = self._gtk.Image("calculator", self._screen.width *.03, self._screen.width *.03)
        squarenumPadButton = Gtk.Button(name ="speed-factor-button")
        squarenumPadButton.connect("clicked", self.open_numpad, self.squareCornerNumberLabel, "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=")
        squarenumPadButton.set_image(squarenumPadIcon)
        squarenumPadButton.set_always_show_image(True)
        
        unitLabel4 = Gtk.Label(_("mm/s"))   
        
        squareCornerNumberLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        squareCornerNumberLabelBox.set_valign(Gtk.Align.CENTER)
        squareCornerNumberLabelBox.set_halign(Gtk.Align.CENTER)
        squareCornerNumberLabelBox.set_name("square-movement-label-box")
        squareCornerNumberLabelBox.pack_end(squarenumPadButton, False, False, 0)
        squareCornerNumberLabelBox.pack_end(self.squareCornerNumberLabel, False, False, 0)
        
        
        squareCornerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        squareCornerBox.set_name("movement-settings-box")
        squareCornerBox.pack_start(squareCornerLabelBox, False, False, 0)
        squareCornerBox.pack_end(unitLabel4, False, True, 0)
        squareCornerBox.pack_end(squareCornerNumberLabelBox, False, False, 0)
        
        movementSettingLabel = Gtk.Label(_("Movement Settings"), name="movement-setting-label")
        movementSettingLabel.set_halign(Gtk.Align.START) 
        movementSettingLabel.set_valign(Gtk.Align.START) 
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_spacing(-10)
        main.pack_start(Gtk.HSeparator(), False, False, 0)
        main.pack_start(AccelerationBox, False, False, 0)
        main.pack_start(Gtk.HSeparator(), False, False, 0)
        main.pack_start(DecelBox, False, False, 0)
        main.pack_start(Gtk.HSeparator(), False, False, 0)
        main.pack_start(velocityBox, False, False, 0)
        main.pack_start(Gtk.HSeparator(), False, False, 0)
        main.pack_start(squareCornerBox, False, False, 0)
        main.pack_start(Gtk.HSeparator(), False, False, 0)

        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.set_vexpand(True)
        page.pack_start(movementSettingLabel, False, False, 20)
        page.pack_start(main, False, False, 0)
        page.pack_end(menu, False, True, 0)
       
        
        self.content.add(page)
    
    
    
    def process_update(self, action, data):
        # if self._printer.state == 'error' or self._printer.state == 'shutdown' or self._printer.state ==  'disconnected':
        #     page_url = 'co_print_home_not_connected_screen'
        #     self._screen.show_panel(page_url, page_url, "Language", 1, False)
            
        if self._printer.state != 'error' :
            if (('toolhead' in data) and ('max_velocity' in data['toolhead'])): 
                machine_velocity = data['toolhead']['max_velocity']
                square_corner_velocity = data['toolhead']['square_corner_velocity']
                max_accel = data['toolhead']['max_accel']
                max_accel_to_decel = data['toolhead']['max_accel_to_decel']
                

                if(self.velocityNumberLabel.get_label() != str(int(machine_velocity))):
                    self.velocityNumberLabel.set_label(str(int(machine_velocity)))
               
                if(self.squareCornerNumberLabel.get_label() != '{:.2f}'.format(float(square_corner_velocity))):
                    self.squareCornerNumberLabel.set_label('{:.2f}'.format(float(square_corner_velocity)))
                
                if(self.accelerationnumberLabel.get_label() != int(max_accel)):
                    self.accelerationnumberLabel.set_label(str(int(max_accel)))
                    self.scaleAcceleration.set_value(int(max_accel))
                if(self.decelnumberLabel.get_label() != int(max_accel_to_decel)):
                    self.decelnumberLabel.set_label(str(int(max_accel_to_decel)))
                    self.scaleDecel.set_value(int(max_accel_to_decel))

    def on_scale_changed(self, scale, label, script):
        
        # Ölçek değeri değiştiğinde çağrılır
        value = int(scale.get_value())
        
        #self.printing.set_fan_speed(self.type,value)
        label.set_label('{:.0f}'.format(value))
        self._screen._ws.klippy.gcode_script(f"{script}{int(value)}")
        
    def open_numpad(self, widget, changedLabel, script):
        
        dialog = KeyPadNew(self)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            resp = dialog.resp
            changedLabel.set_label(resp)
            self._screen._ws.klippy.gcode_script(f"{script}{int(resp)}")
            #self.scale.set_value(int(resp))
            
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
       
        dialog.destroy()