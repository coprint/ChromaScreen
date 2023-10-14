import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib


class HomingDialog(Gtk.Dialog):
    def __init__(self,parent):
        super().__init__(title="My Dialog",parent=None ,flags=0)
        
        self.set_default_size(300, 100)

        title = Gtk.Label("Auto Home Yapılıyor", name="info-dialog-title-label")
        content = Gtk.Label("X,Y ve Z axis’leri başlangıç pozisyonlarına döndürülüyor lütfen bekleyiniz.", name="info-dialog-content-label")
       
        content.set_line_wrap(True)
        content.set_justify(Gtk.Justification.CENTER)

        self.spinner = Gtk.Spinner()
        self.spinner.props.width_request = 50  
        self.spinner.props.height_request = 50
        self.spinner.start()
        
        box = self.get_content_area()
        box.set_spacing(20)
        box.set_name("info-dialog-content-box")
        box.add(title)
        box.add(content)
        box.add(self.spinner)
        self.show_all()
        
   