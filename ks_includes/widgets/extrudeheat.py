import gi
from ks_includes.KlippyGcodes import KlippyGcodes
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
class ExtrudeHeat(Gtk.Box):
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
        downButton.connect("clicked", self.on_button_clicked, '-')
        buttonBox.add(downButton)
        if _zoffsetIconVisibility:
            zOffsetImage = this._gtk.Image("zoffset", this._screen.width *.06, this._screen.width *.06)
            zOffsetImage_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            zOffsetImage_box.set_halign(Gtk.Align.CENTER)
            zOffsetImage_box.add(zOffsetImage)
            zOffsetImage_box.set_name("z-offset-image")
            buttonBox.add(zOffsetImage_box)
        upButton = Gtk.Button(name ="up-down-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)
        upButton.connect("clicked", self.on_button_clicked, '+')
        buttonBox.add(upButton)
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_valign(Gtk.Align.CENTER)
        main.set_halign(Gtk.Align.CENTER)
        #main.set_valign(Gtk.Align.START)
       # main.set_size_request(this._screen.width *.5, -1)
        main.pack_start(labelBox, False, False, 0)
        main.pack_end(buttonBox, False, False, 10)
        self.add(main)

    def on_button_clicked(self, widget, direction):   
        self.printer._screen._ws.klippy.gcode_script(KlippyGcodes.EXTRUDE_REL) 
        self.printer._screen._ws.klippy.gcode_script(KlippyGcodes.extrude(f"{direction}{int(self.printer.extrudeHeatLevel.get_label())}", f"{5 * 60}"), self.finished)   
    
    def updateValue(self, value):
        current_value = value
        self.entry.set_text('{:.2f}'.format(current_value))

    def finished(self,asd,a,b):
        return 