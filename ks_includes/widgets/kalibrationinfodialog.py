import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib


class KalibrationInfoDialog(Gtk.Dialog):
    def __init__(self,parent):
        super().__init__(title="My Dialog",parent=None ,flags=0)
        
        # self.add_buttons(
        #     Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        # )
        self.set_size_request(0, 0)
        self.set_default_size(350, 20)
        pos = self.get_position()
        # Move dialog to the desired location
        self.move(pos[0] + 125, pos[1] + 225)

        title = Gtk.Label(_("Performing Auto Home"), name="info-dialog-title-label")
        content = Gtk.Label(_("X, Y, and Z axes are returning back to their home positions. Please wait."), name="info-dialog-content-label")
       
        content.set_line_wrap(True)
        content.set_justify(Gtk.Justification.CENTER)

        self.spinner = Gtk.Spinner()
        self.spinner.props.width_request = 50  
        self.spinner.props.height_request = 50
        self.spinner.start()
        
        box = self.get_content_area()
        box.set_spacing(15)
        box.set_name("info-dialog-content-box")
        box.add(title)
        box.add(content)
        box.add(self.spinner)
        self.show_all()
        
   