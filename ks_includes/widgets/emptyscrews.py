import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EmptyScrews(Gtk.Dialog):
    def __init__(self, this):
        super().__init__(title="Bed Screws Dialog",parent=None ,flags=0)
        noButton = Gtk.Button(_('Close'),name ="dialog-blue")
        noButton.connect("clicked", self.on_click_button,"cloes")
        self.set_default_size(500, 20)
        pos = self.get_position()
        self.move(pos[0] + 225, pos[1] + 125)
        title = Gtk.Label(_("Set up Screws"), name="info-dialog-title-label")
        content = Gtk.Label('"[bed_screws]” section could not be found in the configuration files. \n You should check Co Print Wiki on the next link. \n https://wiki.coprint3d.com/en/bed_screw-definition ', name="info-dialog-contentt-label")
        content.set_justify(Gtk.Justification.CENTER)
        box = self.get_content_area()
        box.set_spacing(20)
        box.set_name("info-dialog-content-box")
        box.add(title)
        box.add(content)
        box.add(noButton)
        self.show_all()
    def on_click_button(self, widget, response_id):
        self.destroy()
        if response_id == 'close':
            return