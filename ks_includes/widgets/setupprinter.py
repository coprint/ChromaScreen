import json
import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
class SetupPrinterDialog(Gtk.Dialog):
    def __init__(self, this, printerNumber):
        super().__init__(title="Setup Printer Dialog",parent=None ,flags=0)
        self.this = this
        self.printerNumber = printerNumber
        noButton = Gtk.Button(_('Setup Printer'),name ="dialog-blue")
        noButton.connect("clicked", self.on_click_button,"no")
        yesButton = Gtk.Button(_('I had setuped'),name ="dialog-blue")
        yesButton.connect("clicked", self.on_click_button,"yes")
        ButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ButtonBox.pack_start(yesButton, False, False, 0)
        ButtonBox.pack_end(noButton, False, False, 0)
        self.set_default_size(300, 100)
        pos = self.get_position()
        self.move(pos[0] + 345, pos[1] + 100)
        title = Gtk.Label(_("Setup Printer"), name="info-dialog-title-label")
        content = Gtk.Label('Did you setup the printer? Or you want to New setup', name="info-dialog-content-label")
        content.set_line_wrap(True)
        content.set_justify(Gtk.Justification.CENTER)
        content.set_line_wrap(True)
        content.set_justify(Gtk.Justification.CENTER)
        box = self.get_content_area()
        box.set_spacing(20)
        box.set_name("info-dialog-content-box")
        box.add(title)
        box.add(content)
        box.add(ButtonBox)
        self.show_all()
        
    def on_click_button(self, widget, response_id):
        self.destroy()
        if response_id == 'yes':
            try:
                selectedPrinter = 'Printer'+str(self.printerNumber)+'WizardDone'
                f = open(self.this._screen.path_config, encoding='utf-8')
                self.config_data = json.load(f)
                self.config_data[selectedPrinter] = True
                json_object = json.dumps(self.config_data, indent=4)
                with open(self.this._screen.path_config, "w") as outfile:
                    outfile.write(json_object)
            except Exception as e:
                logging.exception(e) 
            self.this._screen.connect_printer('Printer_'+str(self.printerNumber))

        else:
            self.this._screen.selected_wizard_printer = 'Printer'+str(self.printerNumber)+'WizardDone'
            self.this._screen.selected_printer_index = self.printerNumber
            self.this._screen.show_panel("co_print_printing_brand_selection_new", "co_print_printing_brand_selection_new", "Language", 1, False)