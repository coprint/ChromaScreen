import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class PrintFile(Gtk.Box):
  

    def __init__(self, this, _fileName, _filament, _day, fullpath):
        super().__init__()
        
        self.printer = this
        self.thumbnail = this._gtk.Image("file", this._screen.width / 4.5, this._screen.height / 4.5)
        self.thumbnail.get_style_context().add_class("thumbnail")
        
        
        fileNameLabel = Gtk.Label(self.rename_string(_fileName,20), name="printing-files-label-title")
        
        remainingTimeBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        remainingTimeBox.set_valign(Gtk.Align.CENTER)
        dayLabel = Gtk.Label(_day, name="printing-files-label")
        #hourLabel = Gtk.Label(_hour+"saat", name="printing-files-label")
        #minuteLabel = Gtk.Label(_minute+"dakika", name="printing-files-label")
        remainingTimeBox.add(dayLabel)
        #remainingTimeBox.add(hourLabel)
        #remainingTimeBox.add(minuteLabel)
        
        filamentWeight = Gtk.Label(_filament, name="printing-files-label")
        
        
        self.printButton = Gtk.Button(('Print'),name ="print-files-button")
        self.printButton.connect("clicked", this.confirm_print, fullpath)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        buttonBox.set_valign(Gtk.Align.CENTER)
        buttonBox.add(self.printButton)
        
        settingIcon = this._gtk.Image("ayarlar", this._screen.width *.04, this._screen.width *.04)
        settingButton = Gtk.Button(name ="setting-button")
        settingButton.connect("clicked", this.show_rename, f"gcodes/{fullpath}")

        settingButton.set_image(settingIcon)
        settingButton.set_always_show_image(True)
        settingButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        settingButtonBox.set_valign(Gtk.Align.CENTER)
        settingButtonBox.add(settingButton)


       
        self.selectCheck = Gtk.CheckButton()
        self.selectCheck.connect("toggled", self.on_button_toggled, fullpath)
        
        self.main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.main.set_name("print-file-box")
        self.main.set_hexpand(True)
        self.main.set_vexpand(True)
        self.main.pack_start(self.selectCheck, False, False, 5)
        self.main.pack_start(self.thumbnail, False, False, 0)
        self.main.pack_start(fileNameLabel, True, True, 0)
        self.main.pack_start(remainingTimeBox, True, True, 0)
        self.main.pack_start(filamentWeight, True, True, 0)
        self.main.pack_start(buttonBox, False, False, 0)
        self.main.pack_start(settingButtonBox, False, False, 0)
        
        self.add(self.main)
        self.connect("size-allocate", self.on_window_size_changed)

    def rename_string(self, string, length_string):
        if len(string) > length_string:
            res = []
            #return string[:length_string-3] + "..."
            for id in range(0, len(string)):
                if id % 20 == 0 and id != 0:
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
        hbox = self.printer.get_child()
        hbox.set_size_request(width, height)