from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        insertImage = self._gtk.Image("filamentcikis", self._screen.width * .90 , self._screen.width * .50)
        stepLabel = Gtk.Label(_("Step 1 Correction"), name="test-green-label")
        stepLabel.set_halign(Gtk.Align.START)
        testLabel = Gtk.Label(_("Was the filament is extruded?"), name="test-header-white-label")
        testLabel.set_halign(Gtk.Align.START)
        testContentLabel = Gtk.Label(_("Was the filament successfully extruded by the extruder mechanism and did it come out from the bottom without getting stuck?"), name="test-content-white-label")
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
        if value == "yes":
            self._screen._ws.klippy.gcode_script("FILAMENT_CUT")
            self._screen.show_panel("co_print_test_filament_cut", "co_print_test_filament_cut", None, 1,True)
        elif value == "no":
            self._screen.show_panel("co_print_test_error_filament_extrude", "co_print_test_error_filament_extrude", None, 1,True)