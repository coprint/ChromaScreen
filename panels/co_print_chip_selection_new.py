import logging
import os
import subprocess
from ks_includes.widgets.addnetworkdialog import AddNetworkDialog
from ks_includes.widgets.changeMcuSetting import ChangeMCUDialog
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
from kconfiglib import Kconfig
from ks_includes.widgets.checkbuttonboxmcu import CheckButtonBoxMcu
from ks_includes.widgets.binfilegenerateloadingdialog import BinFileGenerateLoadingDialog

from ks_includes.widgets.initheader import InitHeader
from screen import cd
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintChipSelection(*args)



# class CoPrintChipSelection(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
        chips = [
            {'Name': _("MCU Architecture"), 'Page': "co_print_mcu_selection"},
            {'Name': _("Processor Model"), 'Page': "co_print_mcu_model_selection"},
            {'Name': _("Com Interface"), 'Page': "co_print_mcu_com_interface"},
            {'Name': _("Botloader Offset"), 'Page': ""},
            {'Name': _("Clock Referance"), 'Page': ""},
            ]
        
      
       
        initHeader = InitHeader (self, _('Chip Settings'), _('Please select the architecture, communication frequency, clock speed and model of the chip you will be using.'), "mikrochip")

        self.checkButton = CheckButtonBox(self, _('Enable extra low-level configuration options'), self.lowLevelChanged)
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
        
        
       
        #self.checkButton.set_hexpand(True)
 
        checkButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        checkButtonBox.set_halign(Gtk.Align.CENTER)
        checkButtonBox.set_valign(Gtk.Align.CENTER)
        checkButtonBox.pack_start(self.checkButton, False, False, 0)
        checkButtonBox.set_center_widget(self.checkButton)
        

        self.continueButton = Gtk.Button(_('Save'),name ="flat-button-blue")
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
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_wifi_selection')
        self.backButton.set_always_show_image (True)       
        mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainBackButtonBox.pack_start(self.backButton, False, False, 0)

        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(self.scroll, True, True, 0)
        main.pack_end(buttonBox, False, False, 10)
        main.pack_end(checkButtonBox, False, False, 10)
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page.pack_start(mainBackButtonBox, False, False, 0)
        page.pack_start(main, True, True, 0)
     
      
        self.content.add(page)
        self._screen.base_panel.visible_menu(False)

   
    def handleMenu(self):
        if self._screen.kconfig.unique_defined_syms[0].str_value == 'y':
            self.checkButton.set_active(True)
        else:
            self.checkButton.set_active(False)
    
       
        grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=10,
                         row_spacing=10)
        row = 0
        count = 0
        
       
                

        for choice in self._screen.kconfig.choices:
            if choice.visibility != 0:
                
                chipImage = self._gtk.Image("expand-arrow-right", self._gtk.content_width * .05 , self._gtk.content_height * .05)
                chipName = Gtk.Label(self._screen.rename_string(choice.nodes[0].prompt[0],50),name ="wifi-label")
                chipName.set_alignment(0,0.5)
                chipImage.set_alignment(1,0.5)
                
            
                chipBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, name="chip")
                f = Gtk.Frame(name="chip")
                chipBox.pack_start(chipName, False, True, 10)
            
                chipBox.pack_end(chipImage, True, True, 10)
                eventBox = Gtk.EventBox()

                if choice.nodes[0].prompt[0] == "Micro-controller Architecture":
                    pageName = 'co_print_mcu_selection'
                elif choice.nodes[0].prompt[0] == "Processor model":
                    pageName = 'co_print_mcu_model_selection'
                elif choice.nodes[0].prompt[0] == "Communication interface":
                    pageName = 'co_print_mcu_com_interface'
                elif choice.nodes[0].prompt[0] == "Bootloader offset":
                    pageName = 'co_print_mcu_bootloader_ofset'
                elif choice.nodes[0].prompt[0] == "Clock Reference":
                    pageName = 'co_print_mcu_clock_reference'   
                elif choice.nodes[0].prompt[0] == "Processor speed":
                    pageName = 'co_print_baud_rate_selection' 
                elif choice.nodes[0].prompt[0] == "Flash chip":
                    pageName = 'co_print_mcu_flash_chip'
                elif choice.nodes[0].prompt[0] == "Clock Speed":
                    pageName = 'co_print_mcu_clock_speed'
                elif choice.nodes[0].prompt[0] == "Application Address":
                    pageName = 'co_print_mcu_applicaiton_address'

                    
                else:
                    pageName = ''


                eventBox.connect("button-press-event", self.change_page, pageName)
                eventBox.add(chipBox)
                
                f.add(eventBox)
                grid.attach(f, count, row, 1, 1)
                count += 1
                if count % 1 == 0:
                    count = 0
                    row += 1

        # for choice in self._screen.kconfig.menus:
        #     if choice.visibility.visibility != 0:
                
        #         chipImage = self._gtk.Image("expand-arrow-right", self._gtk.content_width * .05 , self._gtk.content_height * .05)
        #         chipName = Gtk.Label(self._screen.rename_string(choice.prompt[0],15),name ="wifi-label")
        #         chipName.set_alignment(0,0.5)
        #         chipImage.set_alignment(1,0.5)
                
            
        #         chipBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40, name="chip")
        #         f = Gtk.Frame(name="chip")
        #         chipBox.pack_start(chipName, False, True, 10)
            
        #         chipBox.pack_end(chipImage, True, True, 10)
        #         eventBox = Gtk.EventBox()

        #         if choice.prompt[0] == "USB ids":
        #             pageName = 'co_print_mcu_usb_ids'
        #         else:
        #             print(choice)
        #             pageName = ''


        #         eventBox.connect("button-press-event", self.change_page, pageName)
        #         eventBox.add(chipBox)
                
        #         f.add(eventBox)
        #         grid.attach(f, count, row, 1, 1)
        #         count += 1
        #         if count % 1 == 0:
        #             count = 0
        #             row += 1

        isUsbPageAdded = False
        isSupportPageAdded = False

        for choice in self._screen.kconfig.unique_defined_syms:
            if choice.visibility != 0 and choice.choice == None and choice.name != 'LOW_LEVEL_OPTIONS':
                
                print(choice.name+ ' ' + choice.nodes[len(choice.nodes)-1].prompt[0] + ' ' + choice.str_value)
                
                chipImage = self._gtk.Image("expand-arrow-right", self._gtk.content_width * .05 , self._gtk.content_height * .05)
                

                if 'USB'  in choice.name :
                
                    if isUsbPageAdded == False:
                       
                      
                        isUsbPageAdded = True
                        name = 'USB ids'
                       
                            
                            
                        chipName = Gtk.Label(self._screen.rename_string(name,50),name ="wifi-label")
                       
                        chipName.set_alignment(0,0.5)
                        chipImage.set_alignment(1,0.5)
                        
                    
                        chipBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, name="chip")
                        f = Gtk.Frame(name="chip")
                        chipBox.pack_start(chipName, False, True, 10)
                    
                        chipBox.pack_end(chipImage, True, True, 10)
                        eventBox = Gtk.EventBox()
                        pageName = 'co_print_mcu_usb_ids'
                        eventBox.connect("button-press-event", self.change_page, pageName)
                        eventBox.add(chipBox)
                        
                        f.add(eventBox)
                        grid.attach(f, count, row, 1, 1)
                        count += 1
                        if count % 1 == 0:
                            count = 0
                            row += 1
                elif 'WANT' in choice.name :
                
                    if isSupportPageAdded == False:
                        isSupportPageAdded = True
                        name = 'Optional features'
                            
                        chipName = Gtk.Label(self._screen.rename_string(name,50),name ="wifi-label")
                       
                        chipName.set_alignment(0,0.5)
                        chipImage.set_alignment(1,0.5)
                        
                    
                        chipBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, name="chip")
                        f = Gtk.Frame(name="chip")
                        chipBox.pack_start(chipName, False, True, 10)
                    
                        chipBox.pack_end(chipImage, True, True, 10)
                        eventBox = Gtk.EventBox()
                        pageName = 'co_print_mcu_optional_feature'
                        eventBox.connect("button-press-event", self.change_page, pageName)
                        eventBox.add(chipBox)
                        
                        f.add(eventBox)
                        grid.attach(f, count, row, 1, 1)
                        count += 1
                        if count % 1 == 0:
                            count = 0
                            row += 1
                else:
                   
                    chipImage.set_alignment(1,0.5)
                    
                
                    chipBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, name="chip")
                    f = Gtk.Frame(name="chip")
                   
                
                    #chipBox.pack_end(chipImage, True, True, 10)s
                    eventBox = Gtk.EventBox()

                    if choice.str_value == 'n' or choice.str_value == 'y':
                        chipName = Gtk.Label(self._screen.rename_string(choice.nodes[len(choice.nodes)-1].prompt[0],50),name ="chip-label")

                        if choice.str_value == 'y':
                             checkButton = CheckButtonBoxMcu(self, self._screen.rename_string(choice.nodes[len(choice.nodes)-1].prompt[0],50), self.mainChoiceChanged, choice.name, True)
                        else:
                             checkButton = CheckButtonBoxMcu(self, self._screen.rename_string(choice.nodes[len(choice.nodes)-1].prompt[0],50), self.mainChoiceChanged, choice.name, False)
                       
                        chipBox.pack_start(checkButton, True, True, 10)
                        chipName.set_alignment(0,0.5)
                        #chipBox.pack_end(chipName, False, True, 10)

                    else:
                        chipName = Gtk.Label('(' + choice.str_value + ') ' +self._screen.rename_string(choice.nodes[len(choice.nodes)-1].prompt[0],50),name ="chip-label")
                        chipName.set_alignment(0,0.5)
                        chipBox.pack_start(chipName, False, True, 10)
                        eventBox.connect("button-press-event", self.openDialog, choice)

                   
                    eventBox.add(chipBox)
                    
                    f.add(eventBox)
                    grid.attach(f, count, row, 1, 1)
                    count += 1
                    if count % 1 == 0:
                        count = 0
                        row += 1

       
        return grid
        
       
    

    


    def lowLevelChanged(self, lowLeveStatus):
       
        if lowLeveStatus:
             self._screen._changeKconfig("LOW_LEVEL_OPTIONS")
        else:
            self._screen._changeKconfigFalse("LOW_LEVEL_OPTIONS")

        for child in self.scroll.get_children():
            self.scroll.remove(child)

        grid = self.handleMenu()

        gridBox = Gtk.Box()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)

        
        
        self.scroll.add(gridBox)
        self.content.show_all()

    def mainChoiceChanged(self, lowLeveStatus, name):
       
        if lowLeveStatus:
             self._screen._changeKconfig(name)
        else:
            self._screen._changeKconfigFalse(name)

       

       
            
    def openDialog(self, a,b, choice):
        
        dialog = ChangeMCUDialog( _('Enter Value'), self,choice.str_value)
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

    def on_click_continue_button(self, continueButton):
        # GLib.idle_add(self.getConf)  
        self.waitDialog = BinFileGenerateLoadingDialog(self)
        self.waitDialog.get_style_context().add_class("bin-generate-dialog")

        self.waitDialog.set_decorated(False)
        self.waitDialog.set_size_request(0, 0)
        response = self.waitDialog.run()
         
        # self._screen.show_panel("co_print_sd_card_selection_process_waiting", "co_print_sd_card_selection_process_waiting", None, 2)        
       
    def close_dialog(self, dialog):
        dialog.response(Gtk.ResponseType.CANCEL)
        dialog.destroy()  


    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)
    
    def change_page(self,a,b,pageName):
        
        self._screen.show_panel(pageName, pageName, None, 2)

    def getConf(self):
        path = self._screen.klipper_path
        
        self._screen.kconfig.write_config(path + "/.config")
        with cd(path):
            # we are in ~/Library
            subprocess.call("make")
       # self.close_dialog(self.waitDialog)