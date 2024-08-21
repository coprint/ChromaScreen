from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        insertImage = self._gtk.Image("chprox", self._screen.width * .50 , self._screen.width * .50)
        stepLabel = Gtk.Label(_("Step 4 "), name="test-green-label")
        stepLabel.set_halign(Gtk.Align.START)
        testLabel = Gtk.Label(_("Control the Proximity Sensor"), name="test-header-white-label")
        testLabel.set_halign(Gtk.Align.START)
        triggerLabel = Gtk.Label(_("Proximitiy Sensor: "), name="test-content-white-label")
        triggerValue = Gtk.Label(_("Not Triggered"), name="test-content-red-label")
        testContentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        testContentBox.pack_start(triggerLabel, False, False, 0)
        testContentBox.pack_start(triggerValue, False, False, 0)
        noButton = Gtk.Button(_('Probe Not Work'),name ="test-button-orange")
        noButton.connect("clicked", self.on_click_button,"no")
        checkButton = Gtk.Button(_('Check Trigger'),name ="test-button-blue")
        checkButton.connect("clicked", self.check_trigger)
        ButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ButtonBox.pack_start(checkButton, False, False, 0)
        ButtonBox.pack_end(noButton, False, False, 20)
        testBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        testBox.set_valign(Gtk.Align.CENTER)
        testBox.pack_start(stepLabel, False, False, 0)
        testBox.pack_start(testLabel, False, False, 0)
        testBox.pack_start(testContentBox, False, False, 0)
        testBox.pack_end(ButtonBox, False, False, 20)
        #----------Main-Box--------
        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main.pack_start(insertImage, True, True, 0)
        main.pack_start(testBox, True, True, 0)
        main.set_halign(Gtk.Align.CENTER)
        main.set_valign(Gtk.Align.CENTER)
        self.content.add(main)
    
    def check_trigger(self, widget):
        self._screen._ws.klippy.gcode_script("QUERY_ENDSTOPS")

    def on_click_button(self,widget,value):
        if value == "yes":
            self._screen.show_panel("co_print_test_chromahead_tools_pass", "co_print_test_chromahead_tools_pass", None, 1,True)
        elif value == "no":
            self._screen.show_panel("co_print_test_error_proximity_sensor", "co_print_test_error_proximity_sensor", None, 1,True)

    def process_update(self, action, data):
        if action == 'notify_gcode_response' and data.startswith("x:"):
            for probe in data.split(" "):
                if probe.split(":")[0] == 'z':
                    if probe.split(":")[1] == 'TRIGGERED':
                        self.on_click_button(None, 'yes')
            