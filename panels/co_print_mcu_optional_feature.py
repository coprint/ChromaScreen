import logging
import os
import subprocess
from ks_includes.widgets.changeMcuSetting import ChangeMCUDialog
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintMcuOptionalFeature(*args)


# class CoPrintMcuOptionalFeature(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
       
        
        self.labels['actions'] = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.labels['actions'].set_hexpand(True)
        self.labels['actions'].set_vexpand(False)
        self.labels['actions'].set_halign(Gtk.Align.CENTER)
        self.labels['actions'].set_homogeneous(True)
        self.labels['actions'].set_size_request(self._gtk.content_width, -1)

       
        initHeader = InitHeader (self, _('Optional Feature'), _('Select the optional features located on the board you will be controlling.'), "mikrochip")

    
        '''diller bitis'''
        
       

        grid = self.handleMenu()
       
        
        gridBox = Gtk.Box()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)
 
        
        self.scroll = self._gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_min_content_height(self._screen.height * .3)
        self.scroll.set_kinetic_scrolling(True)
        self.scroll.get_overlay_scrolling()
    
        
        self.scroll.add(gridBox)
        
        self.checkButton = CheckButtonBox(self, _('USB serial number from CHIPID'),  self.lowLevelChanged)
        
        self.checkButton.set_hexpand(True)
        self.checkButton.set_margin_left(self._gtk.action_bar_width *3)
        self.checkButton.set_margin_right(self._gtk.action_bar_width*3)
        checkButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        #checkButtonBox.pack_start(self.checkButton, False, True, 0)
        checkButtonBox.set_homogeneous(True)
        checkButtonBox.set_halign(Gtk.Align.CENTER)
        checkButtonBox.set_valign(Gtk.Align.CENTER)
        
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
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_chip_selection')
        self.backButton.set_always_show_image (True)       
        mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainBackButtonBox.pack_start(self.backButton, False, False, 0)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(self.scroll, True, True, 0)
        main.pack_end(buttonBox, True, False, 10)
        main.pack_end(checkButtonBox, False, True, 5)
        
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(mainBackButtonBox, False, False, 0)
        page.pack_start(main, True, True, 0)
        
        self.show_restart_buttons()
      
        self.content.add(page)
        self._screen.base_panel.visible_menu(False)
        
    
    

    def lowLevelChanged(self, lowLeveStatus):
       
        if lowLeveStatus:
             self._screen._changeKconfig("USB_SERIAL_NUMBER_CHIPID")
        else:
            self._screen._changeKconfigFalse("USB_SERIAL_NUMBER_CHIPID")

        for child in self.scroll.get_children():
            self.scroll.remove(child)

        grid = self.handleMenu()

        gridBox = Gtk.Box()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)

        
        
        self.scroll.add(gridBox)
        self.content.show_all()


    def handleMenu(self):
        grid = Gtk.Grid(column_homogeneous=True,
                            column_spacing=10,
                            row_spacing=10)
        row = 0
        count = 0
        
        listMcu = []
        
           
        for choice in self._screen.kconfig.unique_defined_syms:
            if choice.visibility != 0 and choice.choice == None and choice.name != 'LOW_LEVEL_OPTIONS':
                
                print(choice.name+ ' ' + choice.nodes[len(choice.nodes)-1].prompt[0] + ' ' + choice.str_value)
                
                
                if 'WANT'  in choice.name :
                    tempChip ={}
                    tempChip['Obj'] = choice
                    
                    listMcu.append(tempChip)
            

        
        for chip in listMcu:
           
                #chipName = Gtk.Label(self._screen.rename_string('(' + chip['Obj'].str_value + ') ' + chip['Obj'].nodes[len(chip['Obj'].nodes)-1].prompt[0],15),name ="wifi-label")
                #chipName.set_alignment(0,0.5)
                
                name = self._screen.rename_string(chip['Obj'].nodes[len(chip['Obj'].nodes)-1].prompt[0],50)
                chipName = Gtk.Label(name,name ="wifi-label")

                if chip['Obj'].str_value == 'y':
                        checkButton = CheckButtonBox(self, name, self.mainChoiceChanged, chip['Obj'].name, True)
                else:
                        checkButton = CheckButtonBox(self, name, self.mainChoiceChanged, chip['Obj'].name, False)
                chipBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40, name="chip")
                chipBox.pack_start(checkButton, True, True, 10)
                chipName.set_alignment(0,0.5)
                #chipBox.pack_end(chipName, False, True, 10)
                
                
               
                
                f = Gtk.Frame(name="chip")
               
                        
                f.add(chipBox)
                grid.attach(f, count, row, 1, 1)
                count += 1
                if count % 1 == 0:
                    count = 0
                    row += 1
            
        return grid

    def mainChoiceChanged(self, lowLeveStatus, name):
       
        if lowLeveStatus:
             self._screen._changeKconfig(name)
        else:
            self._screen._changeKconfigFalse(name)
    
    def openDialog(self, a,b, choice):
        
        dialog = ChangeMCUDialog( choice.nodes[len(choice.nodes)-1].prompt[0], self,choice.str_value)
        dialog.get_style_context().add_class("network-dialog")
        dialog.set_decorated(False)

        response = dialog.run()
 
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
            self._screen._changeKconfigSetValue(choice.name, dialog.psw)
            
            for child in self.scroll.get_children():
                self.scroll.remove(child)
           
            grid = self.handleMenu()


            gridBox = Gtk.Box()
            gridBox.set_halign(Gtk.Align.CENTER)
            gridBox.add(grid)

            
            
            self.scroll.add(gridBox)
            self.content.show_all()


            
        elif response == Gtk.ResponseType.CANCEL:
            subprocess.Popen(["pkill", "onboard"])
            dialog.destroy()

    def eventBoxFunc(self,a,b,obj):
        self.radioButtonSelected(None, obj)
        
    def radioButtonSelected(self, button, selected):
       
        self._screen._changeKconfig(selected.name)
        self._screen.show_panel("co_print_chip_selection", "co_print_chip_selection", None, 1, True)
       
    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_chip_selection", "co_print_chip_selection", None, 1, True)
        
   

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
        
        self._screen.show_panel(data, data, "Language", 1, True)