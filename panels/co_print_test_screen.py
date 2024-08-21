from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
from ks_includes.widgets.initheader import InitHeader
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
         #----------Header-------- 
        initHeader = InitHeader (self, _('Test Screen'))
        #----------Back-Button--------    
        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_advanced_setting_screen')
        self.backButton.set_always_show_image (True)       
        #----------Skip-Button--------        
        skipIcon = self._gtk.Image("forward-arrow", 35, 35)
        skipLabel = Gtk.Label(_("Skip"), name="bottom-menu-label")            
        skipButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        skipButtonBox.set_halign(Gtk.Align.CENTER)
        skipButtonBox.set_valign(Gtk.Align.CENTER)
        skipButtonBox.pack_start(skipLabel, False, False, 0)
        skipButtonBox.pack_start(skipIcon, False, False, 0)
        self.skipButton = Gtk.Button(name ="back-button")
        self.skipButton.add(skipButtonBox)
        self.skipButton.connect("clicked", self.on_click_back_button, "co_print_home_screen")
        self.skipButton.set_always_show_image (True)
        #----------Main-Buttons-------- 
        mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainBackButtonBox.pack_start(self.backButton, False, False, 0)
        #----------Chroma-Pad-Test----------
        chromaPadTestImage = self._gtk.Image("chromapad", self._screen.width * .25, self._screen.width * .50)
        chromaPadTestLabel = Gtk.Label(_("Chroma Pad Test"), name="printer-type-label")
        chromaPadTestBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        chromaPadTestBox.set_halign(Gtk.Align.CENTER)
        chromaPadTestBox.set_valign(Gtk.Align.CENTER)
        chromaPadTestBox.set_name("printer-type-box")
        chromaPadTestBox.pack_start(chromaPadTestImage, False, False, 0)
        chromaPadTestBox.pack_start(chromaPadTestLabel, False, False, 0)
        chromaPadTestEventBox = Gtk.EventBox()
        chromaPadTestEventBox.connect("button-press-event", self.on_chromapad_test)
        chromaPadTestEventBox.add(chromaPadTestBox)
        #--------Chroma-Head-Test-------
        chromaHeadTestImage = self._gtk.Image("testasma", self._screen.width * .25, self._screen.width * .50)
        chromaHeadTestLabel = Gtk.Label(_("Chroma Head Test"), name="printer-type-label")
        chromaHeadTestBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        chromaHeadTestBox.set_halign(Gtk.Align.CENTER)
        chromaHeadTestBox.set_valign(Gtk.Align.CENTER)
        chromaHeadTestBox.set_name("printer-type-box")
        chromaHeadTestBox.pack_start(chromaHeadTestImage, False, False, 0)
        chromaHeadTestBox.pack_start(chromaHeadTestLabel, False, False, 0)
        chromaHeadTestEventBox = Gtk.EventBox()
        chromaHeadTestEventBox.connect("button-press-event", self.on_chromahead_test)
        chromaHeadTestEventBox.add(chromaHeadTestBox)
        #--------Chroma-Head-Test-------
        chromaHeadTestImage1 = self._gtk.Image("chromahead", self._screen.width * .25, self._screen.width * .50)
        chromaHeadTestLabel1 = Gtk.Label(_("Chroma Head Tools Test"), name="printer-type-label")
        chromaHeadTestBox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        chromaHeadTestBox1.set_halign(Gtk.Align.CENTER)
        chromaHeadTestBox1.set_valign(Gtk.Align.CENTER)
        chromaHeadTestBox1.set_name("printer-type-box")
        chromaHeadTestBox1.pack_start(chromaHeadTestImage1, False, False, 0)
        chromaHeadTestBox1.pack_start(chromaHeadTestLabel1, False, False, 0)
        chromaHeadTestEventBox1 = Gtk.EventBox()
        chromaHeadTestEventBox1.connect("button-press-event", self.on_chromahead_test1)
        chromaHeadTestEventBox1.add(chromaHeadTestBox1)
        #----------Tests-Box--------
        testsBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        testsBox.set_halign(Gtk.Align.CENTER)
        testsBox.pack_start(chromaPadTestEventBox, False, False, 0)
        testsBox.pack_start(chromaHeadTestEventBox, False, False, 0)
        testsBox.pack_start(chromaHeadTestEventBox1, False, False, 0)
        #----------Main-Box--------
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main.pack_start(mainBackButtonBox, False, False, 0)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(testsBox, False, False, 0)
        self.content.add(main)

    def on_chromapad_test(self, widget, event):
        self._screen.show_panel("co_print_test_chromapad_touch", "co_print_test_chromapad_touch", "Language", 1, True)

    def on_chromahead_test(self, widget, event):
        self._screen.show_panel("co_print_test_chromahead", "co_print_test_chromahead", "Language", 1, True)
    
    def on_chromahead_test1(self, widget, event):
        self._screen.show_panel("co_print_test_waiting_head", "co_print_test_waiting_head", "Language", 1, True)
        
    def on_click_back_button(self, button, data):
        self._screen.show_panel(data, data, "Language", 1, True)