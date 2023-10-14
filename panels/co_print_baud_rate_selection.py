import logging
import os
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi


from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk

from ks_includes.screen_panel import ScreenPanel


def create_panel(*args):
    return CoPrintChipSelection(*args)


class CoPrintChipSelection(ScreenPanel):

     
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
        chips = [
            {'Name': "9600",  'Button': Gtk.RadioButton()},
            {'Name': "14400",  'Button': Gtk.RadioButton()},
            {'Name': "19200",  'Button': Gtk.RadioButton()},
            {'Name': "38400", 'Button': Gtk.RadioButton()},
            {'Name': "57600", 'Button': Gtk.RadioButton()},
            {'Name': "115200",  'Button': Gtk.RadioButton()},
            {'Name': "128000", 'Button': Gtk.RadioButton()},
            {'Name': "256000", 'Button': Gtk.RadioButton()},
            ]
        
        self.labels['actions'] = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.labels['actions'].set_hexpand(True)
        self.labels['actions'].set_vexpand(False)
        self.labels['actions'].set_halign(Gtk.Align.CENTER)
        self.labels['actions'].set_homogeneous(True)
        self.labels['actions'].set_size_request(self._gtk.content_width, -1)

       
       
        initHeader = InitHeader (self, _('Select Baud Rate'), _('Select the Baud Rate to communicate with the processor you will be using.'), "mikrochip")

        '''diller'''
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
            if count % 2 is 0:
                count = 0
                row += 1


       
        
        gridBox = Gtk.FlowBox()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)
        '''diller bitis'''
        
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
        buttonBox.set_center_widget(self.continueButton)

        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_mcu_flash_chip')
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
        self._screen.show_panel("co_print_sd_card_selection", "co_print_sd_card_selection", None, 2)
        
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, False)
