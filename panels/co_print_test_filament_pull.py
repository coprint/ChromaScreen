from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        insertImage = self._gtk.Image("pullfil", self._screen.width * .90 , self._screen.width * .50)
        stepLabel = Gtk.Label(_("Step 3 Correction"), name="test-green-label")
        stepLabel.set_halign(Gtk.Align.START)
        testLabel = Gtk.Label(_("Pull the filament for the gear tightness test."), name="test-header-white-label")
        testLabel.set_halign(Gtk.Align.START)
        testContentLabel = Gtk.Label(_("The tolerances of the gears will be tested to ensure they can properly grip the filament. When the motor is armed, pull the filament; if it doesn't come out, click Yes. If the filament comes out, click No."), name="test-content-white-label")
        testContentLabel.set_halign(Gtk.Align.START)
        testContentLabel.set_max_width_chars(50)
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
        #----------Main-Box--------
        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main.pack_start(insertImage, True, True, 0)
        main.pack_start(testBox, True, True, 0)
        main.set_halign(Gtk.Align.CENTER)
        main.set_valign(Gtk.Align.CENTER)
        self.content.add(main)

    def on_click_button(self,widget,value):
        self._screen._ws.klippy.gcode_script("G1 E-60 F500")
        if value == "yes":
            self._screen.show_panel("co_print_test_chromahead_passed", "co_print_test_chromahead_passed", None, 1,True)
        elif value == "no":
            self._screen.show_panel("co_print_test_error_filament_pull", "co_print_test_error_filament_pull", None, 1,True)