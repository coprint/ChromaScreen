import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class PrintFile(Gtk.Box):
  

    def __init__(self, this, _fileName, _filament, _day, fullpath):
        super().__init__()
        
        self.printer = this
        self.thumbnail = this._gtk.Image("file", 120, 120)
        self.thumbnail.get_style_context().add_class("thumbnail")
        
        
        fileNameTitle = Gtk.Label(_('Title:'), name="printing-files-label-title")
        fileNameTitleBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        fileNameTitleBox.set_valign(Gtk.Align.START)
        fileNameTitleBox.pack_start(fileNameTitle, False, False, 0)
        fileNameLabel = Gtk.Label(self.rename_string(_fileName,40), name="printing-files-label-content")
        fileBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        fileBox.pack_start(fileNameTitleBox, False, False, 0)
        fileBox.pack_start(fileNameLabel, False, False, 0)

        
        remainingTimeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        remainingTimeBox.set_valign(Gtk.Align.CENTER)
        remainingTimeLabel = Gtk.Label(_('Printing Time:'), name="printing-files-label-title")
        dayLabel = Gtk.Label(_day, name="printing-files-label-content")
        remainingTimeBox.pack_start(remainingTimeLabel, False, False, 0)
        remainingTimeBox.pack_start(dayLabel, False, False, 0)

        filamentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        filamentLabel = Gtk.Label(_('Filament:'), name="printing-files-label-title")
        filamentWeight = Gtk.Label(_filament, name="printing-files-label-content")
        filamentBox.pack_start(filamentLabel, False, False, 0)
        filamentBox.pack_start(filamentWeight, False, False, 0)
        
        
        self.printButton = Gtk.Button(_('Print'),name ="print-files-button")
        self.printButton.connect("clicked", this.confirm_print, fullpath)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        buttonBox.set_valign(Gtk.Align.CENTER)
        buttonBox.add(self.printButton)
        
        # settingIcon = this._gtk.Image("ayarlar", this._screen.width *.04, this._screen.width *.04)
        # settingButton = Gtk.Button(name ="setting-button")
        # settingButton.connect("clicked", this.show_rename, f"gcodes/{fullpath}")

        # settingButton.set_image(settingIcon)
        # settingButton.set_always_show_image(True)
        # settingButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # settingButtonBox.set_valign(Gtk.Align.CENTER)
        # settingButtonBox.add(settingButton)

        contentBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        contentBox.set_valign(Gtk.Align.CENTER)
        contentBox.pack_start(fileBox, False, False, 0)
        contentBox.pack_start(remainingTimeBox, False, False, 0)
        contentBox.pack_start(filamentBox, False, False, 0)
       
        self.selectCheck = Gtk.CheckButton()
        self.selectCheck.connect("toggled", self.on_button_toggled, fullpath)
        
        self.main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.main.set_name("print-file-box")
        self.main.set_hexpand(True)
        self.main.set_vexpand(False)
        self.main.pack_start(self.selectCheck, False, False, 5)
        self.main.pack_start(self.thumbnail, False, False, 0)
        self.main.pack_start(contentBox, False, False, 20)
        self.main.pack_end(buttonBox, False, False, 30)
        # self.main.pack_start(settingButtonBox, False, False, 0)
        
        self.add(self.main)
        #self.connect("size-allocate", self.on_window_size_changed)

    def rename_string(self, string, length_string):
        if len(string) > length_string:
            res = []
            #return string[:length_string-3] + "..."
            for id in range(0, len(string)):
                if id % length_string == 0 and id != 0:
                    res.append('\n')
                res.append(string[id])
            return ''.join(res)
        else:
            return string


    def on_button_toggled(self, button, fullpath):
        
        if button.get_active():
            if fullpath not in self.printer.selectedlist:
                self.printer.selectedlist.append(fullpath)
            print("Radio butonu seçildi:", button.get_label())
        else:
           
            self.printer.selectedlist.remove(fullpath)

        self.printer.selectCheck.set_label(str(len(self.printer.selectedlist)) + ("selected"))

    def checkToggle(self, active):
        self.selectCheck.set_active(active)
    
    def on_window_size_changed(self, widget, event):
        allocation = widget.get_allocation()
        width = allocation.width
        height = allocation.height
        #hbox = self.printer.get_child()
        hbox.set_size_request(width, height)