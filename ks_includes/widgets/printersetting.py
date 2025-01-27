import json
import logging

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PrinterSetting(Gtk.Dialog):
    def __init__(self, this, printerNumber):
        super().__init__(title="Setup Printer Dialog",parent=None ,flags=0)
        self.this = this
        self.printerNumber = printerNumber
        closeIcon = this._gtk.Image("close", this._screen.width *.025, this._screen.width *.025)
        closeButton = Gtk.Button(name ="printing-stop-button")
        closeButton.set_image(closeIcon)
        closeButton.set_always_show_image(True)
        closeButton.connect("clicked", self.on_click_button,"close")
        noButton = Gtk.Button(_('Back to Wizard'),name ="dialog-blue")
        noButton.connect("clicked", self.on_click_button,"no")
        yesButton = Gtk.Button(_('Remove Printer'),name ="dialog-blue")
        yesButton.connect("clicked", self.on_click_button,"yes")
        ButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ButtonBox.pack_start(yesButton, False, False, 0)
        ButtonBox.pack_end(noButton, False, False, 0)
        self.set_default_size(300, 100)
        pos = self.get_position()
        self.move(pos[0] + 300, pos[1] + 100)
        title = Gtk.Label(_("Setup Printer"), name="info-dialog-title-label")
        content = Gtk.Label('Did you remove the printer? Or reset it? ', name="info-dialog-content-label")
        content.set_line_wrap(True)
        content.set_justify(Gtk.Justification.CENTER)
        content.set_line_wrap(True)
        content.set_justify(Gtk.Justification.CENTER)
        titleBox =  Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        titleBox.pack_start(title, False, False, 0)
        titleBox.pack_end(closeButton, False, False, 0)
        box = self.get_content_area()
        box.set_spacing(20)
        box.set_name("info-dialog-content-box")
        box.add(titleBox)
        box.add(content)
        box.add(ButtonBox)
        self.show_all()
    def on_click_button(self, widget, response_id):
        self.destroy()
        if response_id == 'close':
            return
        elif response_id == 'yes':
            try:
                selectedPrinter = 'Printer'+str(self.printerNumber)+'WizardDone'
                f = open(self.this._screen.path_config, encoding='utf-8')
                self.config_data = json.load(f)
                self.config_data[selectedPrinter] = False
                json_object = json.dumps(self.config_data, indent=4)
                with open(self.this._screen.path_config, "w") as outfile:
                    outfile.write(json_object)
            except Exception as e:
                logging.exception(e) 
            try:
                
                f = open(self.this._screen.path_config, encoding='utf-8')
                config_data = json.load(f)
                for key in config_data:
                    for i in range(8):
                        if key == 'Printer'+str(i)+'WizardDone':
                            if config_data[key] == True:
                                self.this._screen.connect_printer('Printer_'+str(i))
                                return
                self.this._screen.restart_firmware()
            except Exception as e:
                logging.exception(e) 
            
        elif response_id == 'no':
            self.this._screen.selected_wizard_printer = 'Printer'+str(self.printerNumber)+'WizardDone'
            self.this._screen.selected_printer_index = self.printerNumber
            self.this._screen.show_panel("co_print_printing_brand_selection_new", "co_print_printing_brand_selection_new", "Language", 1, False)