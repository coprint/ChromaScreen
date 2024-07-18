import logging
import os
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi

from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintPrintingBrandSelection(*args)


# class CoPrintPrintingBrandSelection(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
        initHeader = InitHeader (self, _('Connect Your 3D Printer'), _('Connect your 3D printer to Co Print Smart using a USB cable.'), "yazicibaglama")
        
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
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_printing_selection_port')
        self.backButton.set_always_show_image (True)       
        mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainBackButtonBox.pack_start(self.backButton, False, False, 0)
        
        #treePrinterList--start--
        tree = Gtk.TreeView(name="tree-list")
        
        store = Gtk.TreeStore(bool, str)
        tree.set_model(store)
        
        
        iter1 = store.append(None,[None, "Creality"])
        iter2 = store.append(None, [None, "Anet"])
        iter3 = store.append(None, [None, "Anet"])
        
        
        store.append(iter1, [True, "Creality Ender 3 Pro"])
        store.append(iter1, [False, "Creality Ender 3 V2"])
        store.append(iter1, [False, "Creality CR 10 2017"])
        store.append(iter1, [False, "Creality CR 10 Smart Pro 2022"])
        store.append(iter1, [False, "Creality CR 10 v3"])
        store.append(iter1, [False, "Creality Ender 3 V2"])
        store.append(iter1, [False, "Creality CR 10 2017"])
        store.append(iter1, [False, "Creality CR 10 Smart Pro 2022"])
        store.append(iter1, [False, "Creality CR 10 v3"])
        
        
        store.append(iter2, [None, "Anet a4 2018"])
        store.append(iter2, [None, "Anet a8 2017"])
        store.append(iter2, [None, "Anet a8 2019"])
        store.append(iter2, [None, "Anet E10"])
        store.append(iter2, [None, "Anet E16"])
        store.append(iter2, [None, "Anet a8 2019"])
        store.append(iter2, [None, "Anet E10"])
        store.append(iter2, [None, "Anet E16"])
        
        store.append(iter3, [None, "Anet a4 2018"])
        store.append(iter3, [None, "Anet a8 2017"])
        store.append(iter3, [None, "Anet a8 2019"])
        store.append(iter3, [None, "Anet E10"])
        store.append(iter3, [None, "Anet E16"])
        store.append(iter3, [None, "Anet a8 2019"])
        store.append(iter3, [None, "Anet E10"])
        store.append(iter3, [None, "Anet E16"])
        
        # create a column
        column = Gtk.TreeViewColumn()
        tree.append_column(column)
        # add a toggle render
        toggle = Gtk.CellRendererToggle()
        column.pack_start(toggle, True)
        column.add_attribute(toggle, "active", 0)
        toggle.set_radio(True)
        # and add a text renderer to the same column
        text_ren = Gtk.CellRendererText()
        column.pack_start(text_ren, True)
        column.add_attribute(text_ren, "text", 1)
        
        tree.expand_all()
        select = tree.get_selection()
        select.connect("changed", self.on_tree_selection_changed)
        tree.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        #treePrinterList--end--

        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        #scroll.set_min_content_height(self._screen.height * .3)
        scroll.set_kinetic_scrolling(True)
        scroll.get_overlay_scrolling()

        #scroll.set_hexpand(True)
        scroll.add(tree)
        
        #selectPrinterLabel = Gtk.Label("Listeden yazıcınızı seçiniz")
      
    
        
        selectedPrinterName= Gtk.Label("Creality Ender 3 Pro", name="selected-printer-name")
        selectedPrinterDimension = Gtk.Label(_('Dimension') + ": " + "235mm × 235mm x 300mm", name="selected-printer-dimension")
        selectedPrinterBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        selectedPrinterBox.set_name("selected-printer-box")
        selectedPrinterBox.pack_start(self.image, False, False, 0)
        selectedPrinterBox.pack_start(selectedPrinterName, False, False, 10)
        selectedPrinterBox.pack_start(selectedPrinterDimension, False, False, 0)
        selectedPrinterBox.pack_end(buttonBox, False, False, 5)
        

        pageBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        pageBox.set_name("brand-selection-box")
    
        pageBox.set_halign(Gtk.Align.CENTER)
        pageBox.pack_start(scroll, False, False, 0)
        pageBox.pack_start(selectedPrinterBox, False, False, 0)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        main.pack_start(mainBackButtonBox, False, False, 0)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(pageBox, False, False, 0)
           
       
      
        self.content.add(main)
       
    def radioButtonSelected(self, button, baudRate):
        self.selected = baudRate
    
    
    def on_click_continue_button(self, continueButton):
        self._screen.show_panel("co_print_home_screen", "co_print_home_screen", None, 2)
        
    def on_tree_selection_changed(selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            print("You selected", model[treeiter][0])
            
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, True)
        
   
