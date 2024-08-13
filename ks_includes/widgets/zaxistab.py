import gi
from ks_includes.KlippyGcodes import KlippyGcodes
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
class zAxisTab(Gtk.Box):
    def __init__(self, this, _label, _zoffsetIconVisibility):
        super().__init__()
        self.distance = 50
        self.printer = this
        labelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        labelBox.set_halign(Gtk.Align.CENTER)
        label = Gtk.Label(_label, name="z-axis-label")
        label.set_max_width_chars(6)
        label.set_line_wrap(True)
        label.set_justify(Gtk.Justification.CENTER)   
        labelBox.pack_start(label, False, False, 0)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        buttonBox.set_name("z-axis-tab-button-box")
        downIcon = this._gtk.Image("moveust", this._screen.width *.025, this._screen.width *.025)
        upIcon = this._gtk.Image("movealt", this._screen.width *.025, this._screen.width *.025)
        downButton = Gtk.Button(name ="up-down-tab-buttons")
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
        upButton = Gtk.Button(name ="up-down-tab-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)
        upButton.connect("clicked", self.on_button_clicked, -0.05, '+')
        buttonBox.add(upButton)
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_valign(Gtk.Align.CENTER)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(labelBox, False, False, 0)
        main.pack_end(buttonBox, False, False, 0)
        self.add(main)

    def on_button_clicked(self, widget, value, direction):
            current_value = float(self.printer._printer.data["gcode_move"]["homing_origin"][2])
            new_value = current_value + value
            value = self.distance
            speed = 2
            self.printer._screen._ws.klippy.gcode_script(KlippyGcodes.EXTRUDE_REL)   
            self.printer._screen._ws.klippy.gcode_script( KlippyGcodes.extrude(f"{direction}{self.distance}", f"{speed * 60}")) 
          
    def updateValue(self, value):
        current_value = value
        self.entry.set_text('{:.2f}'.format(current_value))