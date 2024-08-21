from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        insertImage = self._gtk.Image("temperature&fan", self._screen.width * .50 , self._screen.width * .50)
        stepLabel = Gtk.Label(_("Step 3 "), name="test-green-label")
        stepLabel.set_halign(Gtk.Align.START)
        testLabel = Gtk.Label(_("Heating and Hotend Fan"), name="test-header-white-label")
        testLabel.set_halign(Gtk.Align.START)
        temperatureLabel = Gtk.Label(_("Temperature: "), name="test-content-white-label")
        self.temperatureValue = Gtk.Label(0, name="test-content-white-label")
        temperatureBox =Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        temperatureBox.pack_start(temperatureLabel, False, False, 0 )
        temperatureBox.pack_start(self.temperatureValue, False, False, 0 )
        targetLabel = Gtk.Label(_("Target: "), name="test-content-white-label")
        targetValue = Gtk.Label("40", name="test-content-green-label")
        targetBox =Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        targetBox.pack_start(targetLabel, False, False, 0 )
        targetBox.pack_start(targetValue, False, False, 0 )
        statusLabel = Gtk.Label(_("Status: "), name="test-content-white-label")
        self.statusValue = Gtk.Label(_("heating.."), name="test-content-yellow-label")
        statusBox =Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        statusBox.pack_start(statusLabel, False, False, 0 )
        statusBox.pack_start(self.statusValue, False, False, 0 )
        testContentBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        testContentBox.set_halign(Gtk.Align.START)
        testContentBox.set_halign(Gtk.Align.START)
        testContentBox.pack_start(temperatureBox, False, False, 0 )
        testContentBox.pack_start(targetBox, False, False, 0 )
        testContentBox.pack_start(statusBox, False, False, 0 )
        fanTestLabel = Gtk.Label(_("Is Hotend Fan working?"), name="test-header-white-label")
        fanTestLabel.set_halign(Gtk.Align.START)
        yesButton = Gtk.Button(_('Yes'),name ="test-button-green")
        yesButton.connect("clicked", self.on_click_button,"yes")
        noButton = Gtk.Button(_('No'),name ="test-button-orange")
        noButton.connect("clicked", self.on_click_button,"no")
        ButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ButtonBox.pack_start(yesButton, False, False, 0)
        ButtonBox.pack_end(noButton, False, False, 20)
        testBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        testBox.set_valign(Gtk.Align.CENTER)
        testBox.pack_start(stepLabel, False, False, 0)
        testBox.pack_start(testLabel, False, False, 0)
        testBox.pack_start(testContentBox, False, False, 10)
        testBox.pack_start(fanTestLabel, False, False, 10)
        testBox.pack_end(ButtonBox, False, False, 30)
        #----------Main-Box--------
        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main.pack_start(insertImage, True, True, 0)
        main.pack_start(testBox, True, True, 0)
        main.set_halign(Gtk.Align.CENTER)
        main.set_valign(Gtk.Align.CENTER)
        self.content.add(main)

    def on_fan(self, widget, event):
        self._screen._ws.klippy.gcode_script("M104 T0 S40")

    def on_click_button(self,widget,value):
        self._screen._ws.klippy.gcode_script("M104 T0 S0")
        if value == "yes":
            self._screen.show_panel("co_print_test_proximity_sensor", "co_print_test_proximity_sensor", None, 1,True)
        elif value == "no":
            self._screen.show_panel("co_print_test_error_hotend_fan", "co_print_test_error_hotend_fan", None, 1,True)

    def process_update(self, action, data):
        self.temperatureValue.set_label( str(self._printer.get_temp_store('extruder')['temperatures'][-1]))
        if self._printer.get_temp_store('extruder')['temperatures'][-1] >= 40:
            self._screen._ws.klippy.gcode_script("M104 T0 S0")
            self.statusValue.set_label("Heated")