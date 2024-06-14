import logging
import os


import gi

from ks_includes.widgets.initheader import InitHeader
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk

from ks_includes.screen_panel import ScreenPanel


# def create_panel(*args):
#     return CoPrintContractApproval(*args)


# class CoPrintContractApproval(ScreenPanel):
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)

        confidentialityAgreement = Gtk.Label(_("Contract Approval"), name ="contract-approval-label") 
        confidentialityAgreement.set_line_wrap(True)
        confidentialityAgreement.set_max_width_chars(100)
        
        
        initHeader = InitHeader (self, _('Privacy Policy'),_('Please read our agreement and confirm the terms.'), "Privacy")

        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
       # scroll.set_min_content_height(self._screen.height * .3)
        scroll.set_kinetic_scrolling(True)
        scroll.get_overlay_scrolling()
        scroll.add(confidentialityAgreement)
        scroll.set_margin_left(self._gtk.action_bar_width *1)
        scroll.set_margin_right(self._gtk.action_bar_width*1)
      
        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        self.continueButton.set_hexpand(True)
        self.continueButton.set_sensitive(False)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
   
        buttonBox.pack_start(self.continueButton, False, False, 0)

        
        acceptButtonBox = CheckButtonBox(self, _('I have read and accept the Privacy Policy.'), self.oncheck)
        acceptButtonBox.set_halign(Gtk.Align.CENTER)
        
        backIcon = self._gtk.Image("back-arrow", 35, 35)
        backLabel = Gtk.Label(_("Back"), name="bottom-menu-label")            
        backButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        backButtonBox.set_halign(Gtk.Align.CENTER)
        backButtonBox.set_valign(Gtk.Align.CENTER)
        backButtonBox.pack_start(backIcon, False, False, 0)
        backButtonBox.pack_start(backLabel, False, False, 0)
        self.backButton = Gtk.Button(name ="back-button")
        self.backButton.add(backButtonBox)
        self.backButton.connect("clicked", self.on_click_back_button, 'co_print_language_select_screen')
        
        self.backButton.set_always_show_image (True)       
        mainBackButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        mainBackButtonBox.pack_start(self.backButton, False, False, 0)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
     
        main.pack_start(mainBackButtonBox, False, False, 0)
        main.pack_start(initHeader, False, False, 0)
        main.pack_start(scroll, True, True, 5)
        main.pack_end(buttonBox, False, False, 10)
        main.pack_end(acceptButtonBox, False, False, 10)
        

        self.content.add(main)

    def oncheck(self, val):
        self.continueButton.set_sensitive(val)


    def on_click_continue_button(self, continueButton):
        #TODO: buton gtk check boxa dönmeli işaretlenip işaretlenmediği anlaşılmıyor.
        logging.debug(f"contract.approved: 'Accepted'")
        self._screen.show_panel("co_print_region_selection", "co_print_region_selection", None, 1,False)
        
    def on_click_back_button(self, button, data):
        
        self._screen.show_panel(data, data, "Language", 1, False) 
        
        
        
        
  
