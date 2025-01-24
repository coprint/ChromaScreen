import json
import logging

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class FactoryReset(Gtk.Dialog):
    def __init__(self,this):
        super().__init__(title="Bed Screws Dialog",parent=None ,flags=0)
        self.this=this
        closeButton = Gtk.Button(_('Close'),name ="dialog-blue")
        closeButton.connect("clicked", self.on_click_button,"cloes")
        resetButton = Gtk.Button(_('Confirm and Continue Factory Reset'),name ="dialog-blue")
        resetButton.connect("clicked", self.on_click_button,"reset")
        ButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        ButtonBox.pack_start(resetButton, False, False, 0)
        ButtonBox.pack_end(closeButton, False, False, 0)
        self.set_default_size(300, 100)
        pos = self.get_position()
        self.move(pos[0] + 200, pos[1] + 100)
        title = Gtk.Label(_("Factory Reset"), name="info-dialog-title-label")
        content = Gtk.Label('Performing a factory reset will not delete any data. All setup steps and startup pages will be restored to their default state', name="info-dialog-contentt-label")
        content.set_justify(Gtk.Justification.CENTER)
        content.set_line_wrap(True)
        box = self.get_content_area()
        box.set_spacing(20)
        box.set_name("info-dialog-content-box")
        box.add(title)
        box.add(content)
        box.add(ButtonBox)
        self.show_all()
    def on_click_button(self, widget, response_id):
        self.destroy()
        if response_id == 'close':
            return
        elif response_id == 'reset':
            try:
                f = open(self.this._screen.path_config, encoding='utf-8')
                config_data = json.load(f)
                for key in config_data:
                    if config_data[key] == True:
                        config_data[key] = False
                        logging.info(f"Setting {key} to False")
                        
                json_object = json.dumps(config_data, indent=4)
                logging.info(f"{json_object}")
                with open(self.this._screen.path_config, "w") as outfile:
                    outfile.write(json_object)
                    
                self.this._screen.restart_ks()
            except Exception as e:
                logging.exception(e) 