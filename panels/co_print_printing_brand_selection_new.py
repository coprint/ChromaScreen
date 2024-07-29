import logging
import math
import os
from ks_includes.widgets.brandselectdialog import BrandSelectionDialog
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf
import json
from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintPrintingBrandSelection(*args)


# class CoPrintPrintingBrandSelection(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.selected_event_box = None
     
        initHeader = InitHeader (self, _('Connect Your 3D Printer'), _('Connect your 3D printer to Co Print Smart using a USB cable.'))
        
        self.image = self._gtk.Image("printer", self._gtk.content_width * .42 , self._gtk.content_height * .42)
        
        #finish button  
        self.continueButton = Gtk.Button(_('Finish'),name ="flat-button-blue-brand")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        self.continueButton.set_always_show_image (True)
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
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_update_screen')
        self.backButton.set_always_show_image (True)       
        mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainBackButtonBox.pack_start(self.backButton, False, False, 0)
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
        mainBackButtonBox.pack_end(self.skipButton, False, False, 0)

        nextIcon = self._gtk.Image("forward-arrow", 45, 45)
        self.nextButton = Gtk.Button(name ="back-button")
        self.nextButton.add(nextIcon)
        self.nextButton.connect("clicked", self.show_next_page)
        self.nextButton.set_always_show_image (True)   
        nextButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        nextButtonBox.pack_start(self.nextButton, False, False, 0)

        prevIcon = self._gtk.Image("back-arrow", 45, 45)
        self.prevButton = Gtk.Button(name ="back-button")
        self.prevButton.add(prevIcon)
        self.prevButton.connect("clicked", self.show_prev_page)
        self.prevButton.set_always_show_image (True) 
        prevButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        prevButtonBox.pack_start(self.prevButton, False, False, 0)

        
        self.contentMainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        f = open(self._screen.path_brand, encoding='utf-8')
       
        self.data = json.load(f)

        print( self._screen.selected_wizard_printer)



        self.entry = Gtk.Label(xalign=0, name="region-menu-label")
        #self.entry.set_margin_left(20) 
        self.entry.get_style_context().add_class("brand-entry")


        self.listOpenButton = Gtk.Button(image=self._gtk.Image("expand-arrow-down", 50, 50), name ="region-combobox-button")
        self.listOpenButton.connect("clicked", self.on_button_clicked, 1)

        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        vbox.pack_start(self.entry, True, True, 0)
        vbox.pack_end(self.listOpenButton, False, False, 0)
        
        eventBox = Gtk.EventBox()
        eventBox.connect("button-press-event", self.on_button_clicked)
        eventBox.add(vbox)
        
       
        self.page_size = 3
        self.current_page = 0

        self.entry.set_text(self.data[0]['Brand'])
      

       
        self.show_current_page(self.data[0]['Brand'])
        #self.on_combo_changed(self.brand_combo)

        comboBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        comboBox.set_halign(Gtk.Align.START)
        comboBox.pack_start(eventBox, False, False, 82)
        

        sliderBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        sliderBox.pack_start(prevButtonBox, False, False, 0)
        sliderBox.pack_start(self.contentMainBox, False, False, 0)
        sliderBox.pack_start(nextButtonBox, True, True, 0)

        printerSelectButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        printerSelectButtonBox.set_halign(Gtk.Align.CENTER)
        self.selectButton = Gtk.Button(_('Select & Go'),name ="select-button-blue")
        self.selectButton.connect("clicked", self.on_completed)
        self.selectButton.set_hexpand(True)

        self.otherPrintersButton = Gtk.Button(_('Other Printers'),name ="select-button-gray")
        self.otherPrintersButton.connect("clicked", self.on_click_continue_button)
        self.otherPrintersButton.set_hexpand(True)

        printerSelectButtonBox.pack_start(self.selectButton, False, False, 0)
        printerSelectButtonBox.pack_start(self.otherPrintersButton, False, False, 0)

        pageBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        pageBox.set_name("brand-selection-box")
    
        pageBox.set_halign(Gtk.Align.CENTER)
        #pageBox.pack_start(scroll, False, False, 0)
        pageBox.pack_start(comboBox, False, False, 0)
        pageBox.pack_start(sliderBox, False, False, 0)
        pageBox.pack_start(printerSelectButtonBox, False, False, 0)
        
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        main.pack_start(mainBackButtonBox, False, False, 0)
        main.pack_start(initHeader, False, False, 0)
        
        main.pack_start(pageBox, False, False, 0)
           
       
      
        self.content.add(main)

  

    def on_listbox_row_activated(self, listbox, row):
        # Seçilen öğenin değerini Entry kutusuna yazdırma
        selected_value = row.get_child().get_label()
        self.entry.set_text(selected_value)
        self.current_page = 0
        self.show_current_page(selected_value)
        self.dialog.destroy()
    
    def on_button_clicked(self, button, edit):
        
        self.dialog = BrandSelectionDialog(  self, self.data)
        self.dialog.get_style_context().add_class("network-dialog")
        self.dialog.set_decorated(False)

        response = self.dialog.run()
 
        if response == Gtk.ResponseType.OK:
            self.dialog.destroy()
            


            
        elif response == Gtk.ResponseType.CANCEL:
           
            self.dialog.destroy()
    def on_combo_changed(self, combo):
        # ComboBox'taki marka değiştikçe sayfa numarasını sıfırla
        self.current_page = 0
        self.show_current_page(combo)

    def show_current_page(self, text):

        start_index = self.current_page 
        end_index = start_index + self.page_size

        grid = Gtk.Grid(column_homogeneous=True,column_spacing=10,row_spacing=10)
        count = 0

        if self.contentMainBox.get_children() != None:

            for child in self.contentMainBox.get_children():
                self.contentMainBox.remove(child)

        # ComboBox'taki seçili öğeyi al
        self.selected_model = None
        selected_brand = text
        if selected_brand is not None:
            for  model_data in self.data:
                if model_data['Brand'] == selected_brand:
                    for i, model_data in enumerate(model_data['Models'][start_index:end_index]):
                        
                        printerImage = self._gtk.Image(model_data['image'], self._gtk.content_width * .42 , self._gtk.content_height * .42)
                        printerName= Gtk.Label(model_data['name'], name="selected-printer-name")
                        printerDimension = Gtk.Label(_('D.') + ": " + model_data['dimension'], name="selected-printer-dimension")

                        printerBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
                        printerBox.set_name("selected-printer-box")
                        printerBox.pack_start(printerImage, False, True, 5)
                        printerBox.pack_start(printerName, False, False, 5)
                        printerBox.pack_end(printerDimension, True, True, 5)

                        self.eventBox = Gtk.EventBox()
                        self.eventBox.set_name("printer-event-box")
                        self.eventBox.connect("button-press-event", self.event_box_select,model_data)
                        self.eventBox.add(printerBox)
                
                        
                        grid.attach(self.eventBox, count, 0, 1, 1)
                        count += 1     
        gridBox = Gtk.Box()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)
                     

        self.contentMainBox.pack_start(gridBox, False, False, 0)
        self.content.show_all()
        return False
    
    def event_box_select(self, widget, event, model_data):
        if self.selected_event_box:
            self.reset_selected_event_box_style()
        self.selected_model = model_data
        clicked_event_box = widget
        style_context = clicked_event_box.get_style_context()
        style_context.remove_class("printer-event-box")
        style_context.add_class("selected-event-box")
        self.selected_event_box = clicked_event_box
      #  self.eventBox.get_style_context().add_class("printer-event-boxx")
        
    def reset_selected_event_box_style(self):
        # Seçilen EventBox'un stilini sıfırla
        style_context = self.selected_event_box.get_style_context()
        style_context.remove_class("selected-event-box")
        style_context.add_class("printer-event-box")
            
    def show_next_page(self, widget):
        selected_brand = self.entry.get_text()
        listModel = []
        for  model_data in self.data:
            if model_data['Brand'] == selected_brand:
                listModel = model_data['Models']

        if len(listModel)-3 > self.current_page:
            self.current_page += 1
            self.show_current_page(selected_brand)

    def show_prev_page(self, widget):
        selected_brand = self.entry.get_text()
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page(selected_brand)
       
    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate
    
    
    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_chip_selection", "co_print_chip_selection", None, 1, False)
        
    def on_tree_selection_changed(selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:    
            print("You selected", model[treeiter][0])
            
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)
    
    def on_completed(self, continueButton):
        if self.selected_model:
            if self.selected_model['processor'] == 'Atmega':
                self._screen.show_panel("co_print_printers_qr", "co_print_printers_qr", self.selected_model, 1, False)
            else:
                self._screen.show_panel("co_print_sd_card_selection_process_waiting", "co_print_sd_card_selection_process_waiting", self.selected_model, 1, False)
        
   
