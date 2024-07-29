import json
import logging
import gi

from ks_includes.widgets.infodialog import InfoDialog
from ks_includes.widgets.initheader import InitHeader
from ks_includes.widgets.systemsetting import SystemSetting
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ks_includes.screen_panel import ScreenPanel

# def create_panel(*args):
#     return CoPrintPrintingSelectionDone(*args)


# class CoPrintPrintingSelectionDone(ScreenPanel):

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
     
       
        initHeader = InitHeader (self, _('New Update Available'), _("It is recommended to install this update to fix possible errors."), "")

        self.image = self._gtk.Image("update", self._gtk.content_width * .15 , self._gtk.content_height * .15)
        self.ChromaScreenNeedUpdate = self._screen.base_panel.need_update()
        chromaScreenupdate = SystemSetting(self, "ChromaScreen"+" "+_("Current") + " (" + self._screen.version +")", ("Update") , self.ChromaScreenNeedUpdate, 'ChromaScreen')
        updateBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        updateBox.pack_start(self.image, True, True,0)
        updateBox.pack_start(initHeader, False, False, 0)
        updateBox.pack_start(chromaScreenupdate, True, True, 0)
        updateBox.set_valign(Gtk.Align.CENTER)
        updateBox.set_halign(Gtk.Align.CENTER)
        
        self.skipButton = Gtk.Button(_('Skip'),name ="flat-button-gray-skip")
        self.skipButton.connect("clicked", self.on_click_skip_button)
        self.skipButton.set_hexpand(True)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        buttonBox.set_halign(Gtk.Align.CENTER)
        buttonBox.pack_start(self.skipButton, False, False, 0)

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
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main.pack_start(mainBackButtonBox, True, True, 0)
        main.pack_start(updateBox, False, False,0)
        main.pack_end(buttonBox, False, False, 25)
        self.content.add(main)
        self._screen.base_panel.visible_menu(False)
       

    def VersionControl(self, widget, name):
        if name == 'ChromaScreen':
            self._screen.base_panel.open_dialog()

    def refresh_updates(self, widget=None):
        self._screen.show_popup_message(_("Checking for updates, please wait..."), level=1)
        # dialog = InfoDialog(self, "Checking for updates, please wait...", False)
        # dialog.get_style_context().add_class("alert-info-dialog")
        # dialog.set_decorated(False)
        # dialog.run()
        self.ChromaScreenNeedUpdate = self._screen.base_panel.need_update()
        # dialog.destroy()
        self._screen.close_popup_message()
      
    def on_click_skip_button(self, continueButton):
        self._screen.show_panel("co_print_printing_brand_selection_new", "co_print_printing_brand_selection_new", None, 1,True)
        
    def on_click_back_button(self, button, data):
        self._screen.show_panel(data, data, "Language", 1, True)