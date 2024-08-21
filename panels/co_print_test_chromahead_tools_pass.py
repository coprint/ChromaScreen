from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        insertImage = self._gtk.Image("headoky", self._screen.width * .90 , self._screen.width * .50)
        stepLabel = Gtk.Label(_("Step 5 Correction"), name="test-green-label")
        stepLabel.set_halign(Gtk.Align.START)
        testLabel = Gtk.Label(_("Product is Okey"), name="test-header-white-label")
        testLabel.set_halign(Gtk.Align.START)
        continueButton = Gtk.Button(_('Next Product'),name ="test-button-green")
        continueButton.connect("clicked", self.on_click_continue_button)
        ButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ButtonBox.pack_start(continueButton, False, False, 0)
        testBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        testBox.set_valign(Gtk.Align.CENTER)
        testBox.pack_start(stepLabel, False, False, 0)
        testBox.pack_start(testLabel, False, False, 0)
        testBox.pack_end(ButtonBox, False, False, 150)
        #----------Main-Box--------
        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main.pack_start(insertImage, True, True, 0)
        main.pack_start(testBox, True, True, 0)
        main.set_halign(Gtk.Align.CENTER)
        main.set_valign(Gtk.Align.CENTER)
        self.content.add(main)

    def on_click_continue_button(self, connueButton):
        self._screen.show_panel("co_print_test_screen", "co_print_test_screen", None, 1,True)