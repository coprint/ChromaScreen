import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib


class BinFileGenerateLoadingDialog(Gtk.Dialog):
    def __init__(self,parent):
        super().__init__(title="Bİn File Dialog",parent=None ,flags=0)
        
        # self.add_buttons(
        #     Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        # )
        self.set_size_request(0, 0)
        self.set_default_size(400, 0)

        content = Gtk.Label(_("The settings file is being created. During this time.Please wait and do not turn off ChromaScreen."), name="info-dialog-content-label")
        status = Gtk.Label(_("Creating..."), name="bin-generate-dialog-content-label")
       
        content.set_line_wrap(True)
        content.set_justify(Gtk.Justification.CENTER)

        self.spinner = Gtk.Spinner()
        self.spinner.props.width_request = 50  
        self.spinner.props.height_request = 50
        self.spinner.start()
        
        box = self.get_content_area()
        box.set_spacing(20)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)
        box.set_name("bin-generate-dialog-content-box")
        box.add(content)
        box.add(status)
        box.add(self.spinner)
        self.show_all()
        
   