import logging
import os
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel
import pyudev
import psutil
import shutil

# def create_panel(*args):
#     return CoPrintSdCardSelectionProcessWaiting(*args)


# class CoPrintSdCardSelectionProcessWaiting(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, selected_brand_temp):
        super().__init__(screen, selected_brand_temp)
     
        self.selected_brand = selected_brand_temp
        self.initHeader = InitHeader (self, _('Writing to SD Card'), _('Insert the SD Card of your printer into ChromaScreen to change the program of your 3D printer.'), "sdkart")
        self.initHeaderWriting = InitHeader (self, _('Writing to SD Card'), _('Insert the SD Card of your printer into ChromaScreen to change the program of your 3D printer.'), "sdkart")

        self.image = self._gtk.Image("usb-wait", self._gtk.content_width * .4 , self._gtk.content_height * .4)
       
        self.insertedButton = Gtk.Button(_('USB drive has been inserted.'),name ="flat-button-green")
        self.insertedButton.set_hexpand(True)
        self.insertedButton.set_margin_left(self._gtk.action_bar_width *3)
        self.insertedButton.set_margin_right(self._gtk.action_bar_width*3)


        self.writingButton = Gtk.Button(_('Writing the SD card.'),name ="flat-button-yellow")
        self.writingButton.set_hexpand(True)
        self.writingButton.set_margin_left(self._gtk.action_bar_width *3)
        self.writingButton.set_margin_right(self._gtk.action_bar_width*3)

        self.writeDone = Gtk.Button(_('Klipper bin file has been writen.'),name ="flat-button-green")
        #self.writeDone.connect("clicked", self.on_click_continue_button)
        self.writeDone.set_hexpand(True)
        self.writeDone.set_margin_left(self._gtk.action_bar_width *3)
        self.writeDone.set_margin_right(self._gtk.action_bar_width*3)


        self.continueButton = Gtk.Button(_('Please insert the USB drive.'),name ="flat-button-yellow")
        #self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        self.buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.buttonBox.pack_start(self.continueButton, False, False, 0)

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
        self.mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.mainBackButtonBox.pack_start(self.backButton, False, False, 0)
        #----------Skip-Button--------        
        skipIcon = self._gtk.Image("forward-arrow", 35, 35)
        skipLabel = Gtk.Label(_("Skip"), name="bottom-menu-label")            
        skipButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        skipButtonBox.set_halign(Gtk.Align.CENTER)
        skipButtonBox.set_valign(Gtk.Align.CENTER)
        skipButtonBox.pack_start(skipLabel, False, False, 0)
        skipButtonBox.pack_start(skipIcon, False, False, 0)
        self.skipButton = Gtk.Button(name ="back-button")
        self.skipButton.add(skipButtonBox)
        self.skipButton.connect("clicked", self.on_click_back_button, "co_print_home_screen")
        self.skipButton.set_always_show_image (True)       
        self.mainBackButtonBox.pack_end(self.skipButton, False, False, 0)

        self.header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.header.pack_start(self.initHeader, False, False, 0)

        self.main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main.pack_start(self.mainBackButtonBox, False, False, 0)
        self.main.pack_start(self.header, False, False, 0)
        self.main.pack_start(self.image, True, True, 25)
        self.main.pack_end(self.buttonBox, True, False, 15)
        
        
       
      
        self.content.add(self.main)
        self._screen.base_panel.visible_menu(False)


        GLib.idle_add(self.control_usb, None)

   
    def control_usb(self, args):
        self.isSuccess= False
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb')
        device = monitor.poll(timeout=30)
        if device != None:
            
                if device.action == 'add':
                   
                    logging.debug("Inserted!!!!!!!!!!!!:1")
                    self.usbInsertedProcess()
                    self.isSuccess = True
                    logging.debug("Inserted!!!!!!!!!!!!:")
                    self.writingProcess()
                    GLib.timeout_add_seconds(5, self.usbWrite, context, device)
                       
                if device.action == 'unbind':
                    logging.debug('{} unbind'.format(device))
        if self.isSuccess  == False:
            GLib.timeout_add_seconds(1, self.control_usb, None)
        return False
        
                     
       
    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate

    def writingProcess(self):
        logging.debug("Inserted!!!!!!!!!!!!:2")
       
        for child in self.header.get_children():
            self.header.remove(child)
        
        self.header.add(self.initHeaderWriting)

        for child in self.buttonBox.get_children():
            self.buttonBox.remove(child)
        
        self.buttonBox.add(self.writingButton)
        

        svg_file = f"styles/z-bolt/images/usbstickloading.png"
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(svg_file, self._gtk.content_width * .25 , self._gtk.content_height * .25)
        logging.debug("Inserted!!!!!!!!!!!!:3")
        self.image.set_from_pixbuf(pixbuf)
        self.content.show_all()

    def usbInsertedProcess(self):
        logging.debug("Inserted!!!!!!!!!!!!:2")
       
        for child in self.buttonBox.get_children():
            self.buttonBox.remove(child)
        
        self.buttonBox.add(self.insertedButton)

        svg_file = f"styles/z-bolt/images/usbstickokey.png"
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(svg_file, self._gtk.content_width * .25 , self._gtk.content_height * .25)
        logging.debug("Inserted!!!!!!!!!!!!:3")
        self.image.set_from_pixbuf(pixbuf)

        self.content.show_all()
    def usbWrite(self, context, device):
        logging.debug("Inserted!!!!!!!!!!!!")
        try:
            mountpoint = ""
            partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
            logging.debug("All removable partitions: {}".format(", ".join(partitions)))

            sudoPassword = self._screen.pc_password
            command1 = 'mkdir /media/USB-bin'
            pp = os.system('echo %s|sudo -S %s' % (sudoPassword, command1))

            command2 = 'mount -t vfat '+ partitions[0] +' /media/USB-bin -o uid=1000'
            pp = os.system('echo %s|sudo -S %s' % (sudoPassword, command2))
            mountpoint = '/media/USB-bin'
            logging.debug("hbp mountpoint= "+ mountpoint)
            logging.debug("  {}: {}".format(partitions[0], sudoPassword))

            
            logging.debug("Mounted removable partitions:" + str(len(psutil.disk_partitions())))
          
        
            if mountpoint != '':
                if self.selected_brand:
                    source_file = self._screen.path_base_brand + self.selected_brand['fileName']
                    destination_file = mountpoint + '/'

                    source_folder = self._screen.path_base_brand + self.selected_brand['folderName'] + '/.'
                    destination_data_folder =  os.path.join(os.path.expanduser("~/"), "printer_"+str(self._screen.selected_printer_index)+"_data", "config")
                    command_data = 'cp -a '+ source_folder + ' ' +destination_data_folder
                    pp = os.system('echo %s|sudo -S %s' % (sudoPassword, command_data))
                else:

                    source_file = self._screen.klipper_path + '/out'
                    destination_file = mountpoint + '/out'
                              
                # USB belleğinizdeki hedef dosya yolu
               
                logging.debug('cp -r '+ source_file + ' ' +destination_file)
                command2 = 'cp -r '+ source_file + ' ' +destination_file
                pp = os.system('echo %s|sudo -S %s' % (sudoPassword, command2))

               
                
                GLib.timeout_add_seconds(15, self.usbWriteDone)
        except Exception as e:
            logging.exception(e)
            raise RuntimeError(f"Unable to write") from e 
        

    def usbWriteDone(self):
        for child in self.buttonBox.get_children():
            self.buttonBox.remove(child)
        
        self.buttonBox.add(self.writeDone)
        self.content.show_all()
        GLib.timeout_add_seconds(2, self.on_click_continue_button)
       
    
    
    def on_click_continue_button(self):
        self._screen.show_panel("co_print_sd_card_selection", "co_print_sd_card_selection", None, 2)
    
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)
   
