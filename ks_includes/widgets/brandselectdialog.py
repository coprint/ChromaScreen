import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib


class BrandSelectionDialog(Gtk.Dialog):
    def __init__(self,this, data):
        super().__init__(title="My Dialog",parent=None ,flags=0)
        
        # self.add_buttons(
        #     Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        # )
        self.set_size_request(0, 0)
        self.set_default_size(300,320)
        pos = self.get_position()
        # Move dialog to the desired location
        self.move(pos[0] + 128, pos[1] + 190)

       
        self.listbox = Gtk.ListBox(name ="brand")
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        
        for brand in data:
            label = Gtk.Label(label=brand['Brand'], xalign=0, name="info-dialog-brand-label")
            label.set_name("region-label")
            label.set_margin_left(20) 
            label.set_justify(Gtk.Justification.LEFT) 
            label.set_margin_top(10) 
            label.set_margin_bottom(5) 
            self.listbox.add(label)

        self.listbox.set_activate_on_single_click(True)
        self.listbox.connect("row-activated", this.on_listbox_row_activated)


        self.scroll = this._gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_kinetic_scrolling(True)
        self.scroll.get_overlay_scrolling()
      
        self.scroll.add(self.listbox)

        
        
        box = self.get_content_area()
        box.set_spacing(15)
        box.set_name("info-dialog-content-box-brand")
       
        box.add(self.scroll)
        self.show_all()
        
   