import gi
from ks_includes.widgets.keypad_new import KeyPadNew
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
class PercentageFactor(Gtk.Box):
    def __init__(self, this, _image, _label, maxRange, minRange , type):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        #TODO: Change self.printing to self.this
        self.printing = this
        self.type = type
        self.minRange = minRange
        self.maxRange = maxRange
        labelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        image = this._gtk.Image(_image, this._screen.width *.03, this._screen.width *.03)
        label = Gtk.Label(_label, name="zoffset-label")
        labelBox.pack_start(image, True, False, 10)
        labelBox.pack_start(label, True, False, 0)
        labelBox.set_valign(Gtk.Align.START)
        labelBox.set_halign(Gtk.Align.START)
        numPadIcon = this._gtk.Image("calculator", this._screen.width *.04, this._screen.width *.04)
        numPadButton = Gtk.Button(name ="speed-factor-button")
        numPadButton.connect("clicked", self.open_numpad)
        numPadButton.set_image(numPadIcon)
        numPadButton.set_always_show_image(True)
        self.numberLabel = Gtk.Label("0 %", name="percentage-factor-label")
        numberLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        numberLabelBox.set_valign(Gtk.Align.CENTER)
        numberLabelBox.set_halign(Gtk.Align.CENTER)
        numberLabelBox.set_name("percentage-factor-label-box")
        numberLabelBox.add(self.numberLabel)
        inputBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        inputBox.pack_start(numPadButton, False, False, 0)
        inputBox.pack_start(numberLabelBox, True, True, 0)
        speedFactorBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        speedFactorBox.set_hexpand(True)
        speedFactorBox.set_name("speed-factor-box")
        speedFactorBox.set_size_request(-1, this._screen.height*.01)
        speedFactorBox.set_valign(Gtk.Align.START)
        speedFactorBox.pack_start(labelBox, True, True, 0)
        speedFactorBox.pack_end(inputBox, False, True, 0)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.set_name("scale-buttons-box")
        downIcon = this._gtk.Image("arti", this._screen.width *.03, this._screen.width *.03)
        upIcon = this._gtk.Image("eksi", this._screen.width *.03, this._screen.width *.03)
        #downIcon = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size("styles/z-bolt/images/arti.png", this._screen.width *.03, this._screen.width *.03))
        #upIcon = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size("styles/z-bolt/images/eksi.png", this._screen.width *.03, this._screen.width *.03))
        upButton = Gtk.Button(name ="scale-buttons")
        upButton.set_image(upIcon)
        upButton.set_always_show_image(True)
        upButton.connect("clicked", self.up_down_button_clicked, -1)
        buttonBox.add(upButton)
        self.scale = Gtk.Scale()
        self.scale.set_range(0, maxRange)
        self.scale.set_value(100)
        self.scale.set_increments(1, 1)
        self.scale.set_digits(0)
        self.scale.set_draw_value(False)
        self.scale.connect("value-changed", self.on_scale_changed, 1)
        context = self.scale.get_style_context()
        context.add_class("speed-factor-scale")
        buttonBox.pack_start(self.scale, True, True, 0)
        downButton = Gtk.Button(name ="scale-buttons")
        downButton.set_image(downIcon)
        downButton.set_always_show_image(True)
        downButton.connect("clicked", self.up_down_button_clicked, 1)
        buttonBox.add(downButton)
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_hexpand(True)
        main.set_valign(Gtk.Align.START)
        main.set_size_request(this._screen.width *.45, -1)
        main.pack_start(speedFactorBox, True, True, 0)
        main.pack_start(buttonBox, True, True, 0)
        self.add(main)
        
    def up_down_button_clicked(self, widget, value):
            # Mevcut değeri alın
            current_value = self.scale.get_value()
            # Yeni değeri hesaplayın
            new_value = current_value + value
            # Yeni değeri entry'ye ayarlayın
            self.scale.set_value(new_value)
            
    def on_scale_changed(self, scale, a):
        # Ölçek değeri değiştiğinde çağrılır
        value = int(scale.get_value())
        if value < self.minRange:
                value = self.minRange
        if value > self.maxRange:
                value = self.maxRange
        if(value > 0):
            self.printing.set_fan_speed(self.type,value)
        #self.entry.set_text('{:.0f}'.format(value) + '%')
        self.numberLabel.set_label('{:.0f}'.format(value) + '%')
    
    def updateValue(self, value, label):
        self.scale.set_value(value)
        self.numberLabel.set_label('{:.0f}'.format(value) + '%')

    def open_numpad(self, widget):
        dialog = KeyPadNew(self.printing)
        dialog.get_style_context().add_class("new-numpad-dialog")
        dialog.set_decorated(False)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print(dialog.resp)
            resp = int(dialog.resp)
            if resp < self.minRange:
                resp = self.minRange
            if resp > self.maxRange:
                resp = self.maxRange
            self.numberLabel.set_label(str(resp) + "%")
            self.scale.set_value(resp)
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        dialog.destroy()  