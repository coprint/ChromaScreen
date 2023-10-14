import logging
import os
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintMcuComInterface(*args)


class CoPrintMcuComInterface(ScreenPanel):

     
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
        chips = [
            {'Name': "USB (on PA11/PA12)",  'Button': Gtk.RadioButton()},
            {'Name': "Serial (on USART1 PA10/PA9)",  'Button': Gtk.RadioButton()},
            {'Name': "Serial (on USART1 PB7/PB6)",  'Button': Gtk.RadioButton()},
            {'Name': "Serial (on USART2 PA3/PA2)", 'Button': Gtk.RadioButton()},
            {'Name': "Serial (on USART2 PD6/PD5)", 'Button': Gtk.RadioButton()},
            {'Name': "Serial (on USART3 PB11/PB10)",  'Button': Gtk.RadioButton()},
            {'Name': "Serial (on USART3 PD9/PD8)",  'Button': Gtk.RadioButton()},
            {'Name': "CAN bus (on PA11/PA12)",  'Button': Gtk.RadioButton()},
            {'Name': "CAN bus (on PA11/PB9)",  'Button': Gtk.RadioButton()},
            {'Name': "CAN bus (on PA11/PB9)", 'Button': Gtk.RadioButton()}
            ]
        
        self.labels['actions'] = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.labels['actions'].set_hexpand(True)
        self.labels['actions'].set_vexpand(True)
        self.labels['actions'].set_halign(Gtk.Align.CENTER)
        self.labels['actions'].set_homogeneous(True)
        self.labels['actions'].set_size_request(self._gtk.content_width, -1)

       
        initHeader = InitHeader (self, _('Com Interface'), _('Select the com interface model located on the board you will be controlling.'), "mikrochip")

        
        grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=10,
                         row_spacing=10)
        row = 0
        count = 0
        
        group =chips[0]['Button']
        for chip in chips:
            chipName = Gtk.Label(chip['Name'],name ="wifi-label")
            chipName.set_alignment(0,0.5)
            
            chip['Button'] = Gtk.RadioButton.new_with_label_from_widget(group,"")
            if chips[0]['Name'] == chip['Name']:
                 chip['Button'] = Gtk.RadioButton.new_with_label_from_widget(None,"")
           
           
            
            chip['Button'].connect("toggled",self.radioButtonSelected, chip['Name'])
            chip['Button'].set_alignment(1,0.5)
            chipBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40, name="chip")
           
            f = Gtk.Frame(name="chip")
            chipBox.pack_start(chipName, False, True, 10)
           
            chipBox.pack_end(chip['Button'], False, False, 10)
            
            f.add(chipBox)
            grid.attach(f, count, row, 1, 1)
            count += 1
            if count % 1 is 0:
                count = 0
                row += 1


       
        
        gridBox = Gtk.FlowBox()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)
 
        
        self.scroll = self._gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_min_content_height(self._screen.height * .3)
        self.scroll.set_kinetic_scrolling(True)
        self.scroll.get_overlay_scrolling()
        self.scroll.set_margin_left(self._gtk.action_bar_width *2)
        self.scroll.set_margin_right(self._gtk.action_bar_width*2)
        
        self.scroll.add(gridBox)
        
        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.pack_start(self.continueButton, False, False, 0)
        
        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_mcu_clock_reference')
        self.backButton.set_always_show_image (True)       
        mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainBackButtonBox.pack_start(self.backButton, False, False, 0)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(self.scroll, True, True, 0)
        main.pack_end(buttonBox, False, False, 15)
        
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(mainBackButtonBox, False, False, 0)
        page.pack_start(main, True, True, 0)
        
       
      
        self.content.add(page)
        self._screen.base_panel.visible_menu(False)
        
    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate
       
    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_mcu_usb_ids", "co_print_mcu_usb_ids", None, 2)
        
   

    def update_text(self, text):
        
        self.show_restart_buttons()

    def clear_action_bar(self):
        for child in self.labels['actions'].get_children():
            self.labels['actions'].remove(child)

    def show_restart_buttons(self):

        self.clear_action_bar()
        if self.ks_printer_cfg is not None and self._screen._ws.connected:
            power_devices = self.ks_printer_cfg.get("power_devices", "")
            if power_devices and self._printer.get_power_devices():
                logging.info(f"Associated power devices: {power_devices}")
                self.add_power_button(power_devices)

      

    def add_power_button(self, powerdevs):
        self.labels['power'] = self._gtk.Button("shutdown", _("Power On Printer"), "color3")
        self.labels['power'].connect("clicked", self._screen.power_devices, powerdevs, True)
        self.check_power_status()
        self.labels['actions'].add(self.labels['power'])

    def activate(self):
        self.check_power_status()
        self._screen.base_panel.show_macro_shortcut(False)
        self._screen.base_panel.show_heaters(False)
        self._screen.base_panel.show_estop(False)

    def check_power_status(self):
        if 'power' in self.labels:
            devices = self._printer.get_power_devices()
            if devices is not None:
                for device in devices:
                    if self._printer.get_power_device_status(device) == "off":
                        self.labels['power'].set_sensitive(True)
                        break
                    elif self._printer.get_power_device_status(device) == "on":
                        self.labels['power'].set_sensitive(False)

    def firmware_restart(self, widget):
        self._screen._ws.klippy.restart_firmware()

    def restart(self, widget):
        self._screen._ws.klippy.restart()

    def shutdown(self, widget):
        if self._screen._ws.connected:
            self._screen._confirm_send_action(widget,
                                              _("Are you sure you wish to shutdown the system?"),
                                              "machine.shutdown")
        else:
            logging.info("OS Shutdown")
            os.system("systemctl poweroff")

    def restart_system(self, widget):

        if self._screen._ws.connected:
            self._screen._confirm_send_action(widget,
                                              _("Are you sure you wish to reboot the system?"),
                                              "machine.reboot")
        else:
            logging.info("OS Reboot")
            os.system("systemctl reboot")

    def retry(self, widget):
        self.update_text((_("Connecting to %s") % self._screen.connecting_to_printer))
        if self._screen._ws and not self._screen._ws.connecting:
            self._screen._ws.retry()
        else:
            self._screen.reinit_count = 0
            self._screen.init_printer()
        self.show_restart_buttons()

    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, False)