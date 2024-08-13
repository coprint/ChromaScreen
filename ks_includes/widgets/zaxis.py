import gi
from ks_includes.KlippyGcodes import KlippyGcodes
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
class zAxis(Gtk.Box):
    def __init__(self, this, _label, _zoffsetIconVisibility):
        super().__init__()
        self.printer = this
        labelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        labelBox.set_halign(Gtk.Align.CENTER)
        label = Gtk.Label(_label, name="z-axis-label")
        label.set_max_width_chars(6)
        label.set_line_wrap(True)
        label.set_justify(Gtk.Justification.CENTER)
        labelBox.pack_start(label, False, False, 0)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        buttonBox.set_name("z-axis-button-box")
        downIcon = this._gtk.Image("moveust", this._screen.width *.06, this._screen.width *.06)
        upIcon = this._gtk.Image("movealt", this._screen.width *.06, this._screen.width *.06)
        downButton = Gtk.Button(name ="up-down-buttons")
        downButton.set_image(downIcon)
        downButton.set_always_show_image(True)
        downButton.connect("clicked", self.on_button_clicked, 0.05, '-')
        buttonBox.add(downButton)
        if _zoffsetIconVisibility:
            zOffsetImage = this._gtk.Image("zoffset", this._screen.width *.06, this._screen.width *.06)
            zOffsetImage_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
            zOffsetImage_box.set_halign(Gtk.Align.CENTER)
            zOffsetImage_box.add(zOffsetImage)
            zOffsetImage_box.set_name("z-offset-image")
            buttonBox.add(zOffsetImage_box)
        upButton = Gtk.Button(name ="up-down-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)
        upButton.connect("clicked", self.on_button_clicked, -0.05, '+')
        buttonBox.add(upButton)
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_valign(Gtk.Align.CENTER)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(labelBox, False, False, 0)
        main.pack_end(buttonBox, False, False, 10)      
        self.add(main)

    def on_button_clicked(self, widget, value, direction):
            current_value = float(self.printer._printer.data["gcode_move"]["homing_origin"][2])
            new_value = current_value + value
            if(self.printer.distance):
                 value = self.printer.distance
            if hasattr(self.printer, "speed"):
                if(self.printer.speed == 'Slow'):
                    speed = 1
                elif(self.printer.speed == 'Normal'):
                     speed = 2
                elif(self.printer.speed == 'High'):
                     speed = 5
                else:
                     speed = int(self.printer.speed)
                self.printer._screen._ws.klippy.gcode_script(KlippyGcodes.EXTRUDE_REL)   
                self.printer._screen._ws.klippy.gcode_script( KlippyGcodes.extrude(f"{direction}{self.printer.distance}", f"{speed * 60}")) 
                #self.printer._screen._ws.klippy.gcode_script(KlippyGcodes.extrude(f"{direction}{self.printer.distance}"), 'T1')   
            else:
                    if direction == '-':
                         direction_temp = '+'
                    else:
                         direction_temp = '-'     
                    if hasattr(self.printer, "move"):
                        self.printer.move(None, 'Z', direction_temp)
                    else:
                        self.printer._screen._ws.klippy.gcode_script(f"SET_GCODE_OFFSET Z_ADJUST={direction_temp}{abs(value)} MOVE=1")

    def updateValue(self, value):
        current_value = value
        self.entry.set_text('{:.2f}'.format(current_value))