from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        insertImage = self._gtk.Image("error", self._screen.width * .50 , self._screen.width * .30)
        stepLabel = Gtk.Label(_("Step 2 Error"), name="test-orange-label")
        stepLabel.set_halign(Gtk.Align.START)
        testLabel = Gtk.Label(_("Filament Cut Failed"), name="test-header-white-label")
        testLabel.set_halign(Gtk.Align.START)
        testContentLabel = Gtk.Label(_("A problem has been encountered, please set this product aside."), name="test-content-white-label")
        testContentLabel.set_max_width_chars(60)
        testContentLabel.set_line_wrap(True)
        testContentLabel.set_halign(Gtk.Align.START)
        continueButton = Gtk.Button(_('Return to Start'),name ="test-button-orange")
        continueButton.connect("clicked", self.on_click_continue_button)
        ButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ButtonBox.pack_start(continueButton, False, False, 0)
        testBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        testBox.set_valign(Gtk.Align.CENTER)
        testBox.set_halign(Gtk.Align.CENTER)
        testBox.pack_start(stepLabel, False, False, 0)
        testBox.pack_start(testLabel, False, False, 0)
        testBox.pack_start(testContentLabel, False, False, 0)
        testBox.pack_end(ButtonBox, False, False, 30)
        #----------Main-Box--------
        hBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
        hBox.pack_start(insertImage, True, True, 0)
        hBox.pack_start(testBox, True, True, 0)
        hBox.set_valign(Gtk.Align.CENTER)
        hBox.set_halign(Gtk.Align.CENTER)
        vBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vBox.pack_start(hBox, False, False, 100)
        vBox.set_valign(Gtk.Align.CENTER)
        vBox.set_halign(Gtk.Align.CENTER)
        self.content.add(vBox)

    def on_click_continue_button(self, connueButton):
        self._screen.show_panel("co_print_test_screen", "co_print_test_screen", None, 1,True)