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
#("We have a 14-day return policy, which means you have 14 days after receiving your item to request a return.\n"+"To be eligible for a return, your item must be in the same condition that you received it, unworn or unused, with tags, and in its original packaging. You’ll also need the receipt or proof of purchase. To start a return, you can contact us at coprint3d@gmail.com. Please note that returns will need to be sent to the address which will send.\n"+"If your return is accepted, we’ll send you a return shipping label, as well as instructions on how and where to send your package. Items sent back to us without first requesting a return will not be accepted. You can always contact us for any return question at coprint3d@gmail.com.\n"+"Damages and issuesPlease inspect your order upon reception and contact us immediately if the item is defective, damaged or if you receive the wrong item, so that we can evaluate the issue and make it right.\n"+"Unfortunately, we cannot accept returns on sale items or gift cards.\n"+"ExchangesThe fastest way to ensure you get what you want is to return the item you have, and once the return is accepted, make a separate purchase for the new item.\n"+"European Union 14 day cooling off periodNotwithstanding the above, if the merchandise is being shipped into the European Union, you have the right to cancel or return your order within 14 days, for any reason and without a justification. As above, your item must be in the same condition that you received it, unworn or unused, with tags, and in its original packaging with unopening. You’ll also need the receipt or proof of purchase.")
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
        
        self._screen.show_panel(data, data, "Language", 1, True) 
        
        
        
        
  
