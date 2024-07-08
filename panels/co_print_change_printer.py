import json
import logging
import os
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi

from ks_includes.widgets.printerdetail import PrinterDetail

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintChangePrinter(*args)


class CoPrintChangePrinter(ScreenPanel):
# class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

       

        printers = self._config.get_printers()

        printer_grid = Gtk.Grid()
        printer_grid.set_row_spacing(20)
        printer_grid.set_column_spacing(20)
        left = 0
        top = 0


        self.config_data = None
        
        try:
            f = open(self._screen.path_config, encoding='utf-8')
       
            self.config_data = json.load(f)
        except Exception as e:
            logging.exception(e) 

        for i, printer in enumerate(printers):
            printer_status_style = "printer-status-not-working"
            
            if self.config_data['Printer'+str(i+1)+'WizardDone'] == False:
                printer_status_style = "printer-status-not-configured"
                name = 'None'
                state = 'Not Installed Yet'
            elif printer['data'].state == 'ready':
                printer_status_style = "printer-status-paused"
                state =  _(printer['data'].state)
                name = list(printer)[0]
            elif printer['data'].state == 'printing':
                printer_status_style = "printer-status-continuing"
                name = list(printer)[0]
                state =  _(printer['data'].state)
            else:
                name = list(printer)[0]
                state =  _(printer['data'].state)

            printingDetail = PrinterDetail(self, name, (i + 1), state, printer_status_style,
                                           "printer-"+ str(i+1))
            printer_grid.attach(printingDetail, left, top, 1, 1)
            if left == 0:
                left = 1
            else:
                left = 0
                top += 1



        printerBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        printerBox.set_vexpand(True)
        printerBox.set_valign(Gtk.Align.CENTER)
        printerBox.set_halign(Gtk.Align.CENTER)
        printerBox.pack_start(printer_grid, False, False, 0)

        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_kinetic_scrolling(True)
        scroll.get_overlay_scrolling()
        scroll.set_hexpand(True)
        scroll.add(printerBox)

        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.pack_start(scroll, True, True, 0)
        main.pack_end(BottomMenu(self, False), False, True, 0)

        self.content.add(main)

    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate

    def on_button_toggled(self, button):

        if button.get_active():
            print("Radio butonu seçildi:", button.get_label())

    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_printing_selection_port", "co_print_printing_selection_port", None, 2)
