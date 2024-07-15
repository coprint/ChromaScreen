import os
import gi
from gi.repository import Gtk 
from ks_includes.screen_panel import ScreenPanel
from ks_includes.widgets.initheader import InitHeader

class Panel(ScreenPanel):
    def __init__(self, screen, printer_data):
        super().__init__(screen, printer_data)
        self.selected_printer = printer_data
        self.firmware = False
        self.configFiles = False
        #----------Header-------- 
        initHeader = InitHeader (self, _('Scan the QR Code'))
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
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_printing_brand_selection_new')
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
        mainBackButtonBox.pack_end(self.skipButton, False, False, 0)
        #----------firmware-Box--------
        firmwareBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        firmwareLabel = Gtk.Label(_("The printer's firmware has been changed"), name="wiki-header-white-label")
        firmwareBox.set_halign(Gtk.Align.CENTER)
        firmwareBox.set_valign(Gtk.Align.CENTER)
        self.firmwareCheck = Gtk.CheckButton("", name="check-box")
        self.firmwareCheck.connect("toggled", self.on_toggled, "firmware")
        firmwareBox.pack_start(firmwareLabel, False, False, 0)
        firmwareBox.pack_start(self.firmwareCheck, False, False, 0)
        #----------Config-Files-Box--------
        configFilesBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        configFilesLabel = Gtk.Label(_("The Config Files have been uploaded"), name="wiki-header-white-label")
        configFilesBox.set_halign(Gtk.Align.CENTER)
        configFilesBox.set_valign(Gtk.Align.CENTER)
        self.configFilesCheck = Gtk.CheckButton("", name="check-box")
        self.configFilesCheck.connect("toggled", self.on_toggled, "configFiles")
        configFilesBox.pack_start(configFilesLabel, False, False, 0)
        configFilesBox.pack_start(self.configFilesCheck, False, False, 0)
        #----------printer-Box--------
        printerImage = self._gtk.Image(self.selected_printer['image'], 120, 120)
        printerLabel = Gtk.Label((self.selected_printer["name"]), name="wiki-header-white-label")
        printFirstContentLabel = Gtk.Label(_("This printer is an Atmega-based processor printer. You can access the steps required to write the '.Hex' files to the printer by scanning the QR Code."), name="wiki-content-white-label")
        printSecondContentLabel = Gtk.Label(_("After completing the steps, connect the printer to ChromaPad by clicking Next Step."), name="wiki-content-white-label")
        printerLabelsBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        printerLabelsBox.set_halign(Gtk.Align.CENTER)
        printerLabelsBox.set_valign(Gtk.Align.CENTER)
        printerLabelsBox.pack_start(printerLabel, False, False, 0)
        printerLabelsBox.pack_start(printFirstContentLabel, False, False, 0)
        printerLabelsBox.pack_start(firmwareBox, False, False, 0)
        printerLabelsBox.pack_start(configFilesBox, False, False, 0)
        printerLabelsBox.pack_start(printSecondContentLabel, False, False, 0)
        printerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        printerBox.set_name("wiki-white-box")
        printerBox.set_halign(Gtk.Align.CENTER)
        printerBox.set_valign(Gtk.Align.CENTER)
        printerBox.pack_start(printerImage, False, False, 0)
        printerBox.pack_start(printerLabelsBox, False, False, 0)
         #----------QR-Image-------- 
        printerQr = self._gtk.Image("atmage-qr", 120, 120)
        wikiHeaderLabel = Gtk.Label(_("Co Print Wiki"), name="wiki-header-white-label")
        wikiContentLabel = Gtk.Label("wiki.coprint3d.com/en/atmega", name="wiki-content-white-label")
        wikiContentLabel.set_max_width_chars(30)
        wikiContentLabel.set_line_wrap(True)
        wikiContentLabel.set_justify(Gtk.Justification.CENTER)
        wikiContentLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        wikiContentLabelBox.pack_start(wikiContentLabel, False, False, 0)
        wikiBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        wikiBox.set_halign(Gtk.Align.CENTER)
        wikiBox.set_name("wiki-white-box")
        wikiBox.pack_start(printerQr, False, False, 0)  
        wikiBox.pack_start(wikiHeaderLabel, False, False, 0)
        wikiBox.pack_start(wikiContentLabelBox, False, False, 0)
        #----------Page-Box--------
        pageBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        pageBox.set_name("brand-selection-box")
        pageBox.set_halign(Gtk.Align.CENTER)
        pageBox.pack_start(printerBox, False, False, 0)
        pageBox.pack_start(wikiBox, False, False, 0)
        #----------Next-Button--------   
        self.nextButton = Gtk.Button(_('Next Step'),name ="select-button-blue")
        self.nextButton.connect("clicked", self.on_click_continue_button)
        self.nextButton.set_hexpand(True)
        self.nextButton.set_always_show_image (True)
        #----------Upload-Button--------   
        self.uploadButton = Gtk.Button(_('Upload Conf files'),name ="select-button-blue")
        self.uploadButton.connect("clicked", self.upload_config_files)
        self.uploadButton.set_hexpand(True)
        self.uploadButton.set_always_show_image (True)
        #----------Continue-Buttons--------
        continueButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        continueButtonBox.pack_start(self.nextButton, False, False, 0)
        continueButtonBox.pack_start(self.uploadButton, False, False, 0)
        #----------Main-Box--------
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.pack_start(mainBackButtonBox, False, False, 0)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(pageBox, False, False, 0)
        main.pack_start(continueButtonBox, False, False, 0)
        self.content.add(main)
        
    def on_toggled(self, button, name):
        if name == "firmware":
            if button.get_active():
                self.firmware = True
            else:
                self.firmware = False
        if name == "configFiles":
            if button.get_active():
                self.configFiles = True
            else:
                self.configFiles = False

    def upload_config_files(self, button):
        if self.selected_brand:
            sudoPassword = self._screen.pc_password
            source_folder = self._screen.path_base_brand + self.selected_brand['folderName'] + '/.'
            destination_data_folder =  os.path.join(os.path.expanduser("~/"), "printer_"+str(self._screen.selected_printer_index)+"_data", "config")
            command_data = 'cp -a '+ source_folder + ' ' +destination_data_folder
            pp = os.system('echo %s|sudo -S %s' % (sudoPassword, command_data))
            self.configFilesCheck.set_active(True)
            self.on_toggled(self.configFilesCheck, "configFiles")

    def on_click_continue_button(self, continueButton):
        if self.firmware and self.configFiles:
            self._screen.show_panel("co_print_printing_selection_port", "co_print_printing_selection_port", None, 2)

    def on_click_back_button(self, button, data):
        self._screen.show_panel(data, data, "Language", 1, False)