from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.fan_on = False
        insertImage = self._gtk.Image("controlthefan", self._screen.width * .90 , self._screen.width * .50)
        stepLabel = Gtk.Label(_("Step 2 "), name="test-green-label")
        stepLabel.set_halign(Gtk.Align.START)
        testLabel = Gtk.Label(_("Control the Main Fan"), name="test-header-white-label")
        testLabel.set_halign(Gtk.Align.START)
        testContentLabel = Gtk.Label(_("Click the Start Fan button to turn on the main fan. If the fan is spinning successfully, click Yes; if it’s not spinning, click No."), name="test-content-white-label")
        testContentLabel.set_halign(Gtk.Align.START)
        testContentLabel.set_max_width_chars(40)
        testContentLabel.set_line_wrap(True)
        testContentLabel.set_halign(Gtk.Align.START)
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
        testBox.pack_start(testContentLabel, False, False, 0)
        testBox.pack_end(ButtonBox, False, False, 30)
        fanImage = self._gtk.Image("fanayari", self._screen.width * .25 , self._screen.width * .10)
        fanImageBox = Gtk.EventBox()
        fanImageBox.set_name("fan-test-box")
        fanImageBox.set_halign(Gtk.Align.CENTER)
        fanImageBox.set_valign(Gtk.Align.CENTER)
        fanImageBox.connect("button-press-event", self.on_fan)
        fanImageBox.add(fanImage)
        #----------Main-Box--------
        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main.pack_start(insertImage, True, True, 0)
        main.pack_start(testBox, True, True, 0)
        main.pack_start(fanImageBox, True, True, 10)
        main.set_halign(Gtk.Align.CENTER)
        main.set_valign(Gtk.Align.CENTER)
        self.content.add(main)

    def on_fan(self, widget, event):
        if self.fan_on:
            self.fan_on = False
            self._screen._ws.klippy.gcode_script("M106 S0")
        else:
            self.fan_on = True
            self._screen._ws.klippy.gcode_script("M106 S255")

    def on_click_button(self,widget,value):
        self._screen._ws.klippy.gcode_script("M106 S0")
        if value == "yes":
            self._screen._ws.klippy.gcode_script("M104 T0 S40")
            self._screen.show_panel("co_print_test_hotend_fan", "co_print_test_hotend_fan", None, 1,True)
        elif value == "no":
            self._screen.show_panel("co_print_test_error_main_fan", "co_print_test_error_main_fan", None, 1,True)