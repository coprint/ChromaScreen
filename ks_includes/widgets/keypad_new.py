import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
class KeyPadNew(Gtk.Dialog):
    def __init__(self, this):
        super().__init__(title="My Dialog", parent=None, flags=0)
         # Get current position of dialog
        pos = self.get_position()
        # Move dialog to the desired location
        self.move(pos[0] + 345, pos[1] + 100)
        self.labels = {}
        self.resp = 0
        numpad = Gtk.Grid()
        numpad.set_direction(Gtk.TextDirection.LTR)
        numpad.get_style_context().add_class('numpad-new')
        keys = [
            ['1', 'numpad_tleft'],
            ['2', 'numpad_top'],
            ['3', 'numpad_tright'],
            ['4', 'numpad_left'],
            ['5', 'numpad_button'],
            ['6', 'numpad_right'],
            ['7', 'numpad_left'],
            ['8', 'numpad_button'],
            ['9', 'numpad_right'],
            ['B', 'numpad_bleft'],
            ['0', 'numpad_bottom'],
            ['E', 'numpad_bright']
        ]
        for i in range(len(keys)):
            k_id = f'button_{str(keys[i][0])}'
            if keys[i][0] == "B":
                deleteIcon = this._gtk.Image("trash", this._screen.width *.03, this._screen.width *.03)
                deleteButton = Gtk.Button(name ="numpad-delete-button")
                deleteButton.set_image(deleteIcon)
                deleteButton.set_always_show_image(True)
                self.labels[k_id] = deleteButton
            elif keys[i][0] == "E":
                completeIcon = this._gtk.Image("approve", this._screen.width *.03, this._screen.width *.03)
                completeButton = Gtk.Button(name ="numpad-approve-button")
                completeButton.set_image(completeIcon)
                completeButton.set_always_show_image(True)
                self.labels[k_id] = completeButton
            else:
                self.labels[k_id] = Gtk.Button(label=keys[i][0])
            self.labels[k_id].connect('clicked', self.update_entry, keys[i][0])
            self.labels[k_id].get_style_context().add_class("numpad-new-button")
            numpad.attach(self.labels[k_id], i % 3, i / 3, 1, 1)
        self.labels["keypad"] = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.labels['entry'] = Gtk.Entry()
        self.labels['entry'].get_style_context().add_class("numpad-new-label")
        self.labels['entry'].props.xalign = 0.5
        self.labels['entry'].connect("activate", self.update_entry, "E")
        entryBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        entryBox.set_name("numpad-entry-box")
        entryBox.pack_start(self.labels['entry'], True, True, 0)
        closeIcon = this._gtk.Image("keypad-close", this._screen.width *.03, this._screen.width *.03)
        closeButton = Gtk.Button(name ="numpad-close-button")
        closeButton.set_image(closeIcon)
        closeButton.set_always_show_image(True)
        closeButton.connect("clicked", lambda x: self.destroy())
        closeButton.set_halign(Gtk.Align.END)  # Kapatma düğmesini sağa hizala
        closeButton.set_valign(Gtk.Align.START)  # Kapatma düğmesini yukarı hizala
        labelandbuttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        labelandbuttonBox.set_name("keypad-dialog-content")
        labelandbuttonBox.set_spacing(10)
        labelandbuttonBox.add(entryBox)
        labelandbuttonBox.add(numpad)
        box = self.get_content_area()
        box.set_name("keypad-dialog")
        box.pack_start(closeButton, False, False, 0)
        box.add(labelandbuttonBox)
        self.show_all()
        self.labels["keypad"] = numpad
        
    def clear(self):
        self.labels['entry'].set_text("")

    def update_entry(self, widget, digit):
        text = self.labels['entry'].get_text()
        if digit == 'B':
            if len(text) < 1:
                return
            self.labels['entry'].set_text(text[:-1])
        elif digit == 'E':
            self.response(Gtk.ResponseType.OK)
            try:
                temp = text
            except ValueError:
                temp = 0
            self.resp = temp
            self.labels['entry'].set_text("")
        elif len(text) >= 6:
            return
        else:
            self.labels['entry'].set_text(text + digit)