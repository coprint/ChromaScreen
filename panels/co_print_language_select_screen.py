import os
import gi
from ks_includes.widgets.initheader import InitHeader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):     
    def __init__(self, screen, title):
        super().__init__(screen, title)
        self.languages = [
            {'Lang':'en' ,'Name': _('English'), 'Icon': 'English', 'Button': Gtk.RadioButton()},
            {'Lang':'fr' ,'Name': _('French'), 'Icon': 'France', 'Button': Gtk.RadioButton()},
            {'Lang':'de' ,'Name': _("Deutsch"), 'Icon': 'Germany', 'Button': Gtk.RadioButton()},
            {'Lang':'tr' ,'Name': _("Turkish"), 'Icon': 'Turkey', 'Button': Gtk.RadioButton()},
            {'Lang':'it' ,'Name': _('Italian'), 'Icon': 'Italy', 'Button': Gtk.RadioButton()},
            {'Lang':'es' ,'Name': _('Spanish'), 'Icon': 'Spain', 'Button': Gtk.RadioButton()},
            ]
        self.lang_changed = False
        self.labels['actions'] = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.labels['actions'].set_hexpand(True)
        self.labels['actions'].set_vexpand(False)
        self.labels['actions'].set_halign(Gtk.Align.CENTER)
        self.labels['actions'].set_homogeneous(True)
        self.labels['actions'].set_size_request(self._gtk.content_width, -1)
        initHeader = InitHeader (self, _('Language Settings'), _('Please specify the system language'), "Geography")
        grid = Gtk.Grid(column_homogeneous=True,
                        column_spacing=10,
                        row_spacing=10)
        row = 0
        count = 0
        self.group =  self.languages[0]['Button']
        self.new_lang = None
        self.current_lang =  self._config.current_lang
        for language in self.languages:
            languageImage = self._gtk.Image(language['Icon'], self._gtk.content_width * .05 , self._gtk.content_height * .05)
            languageName = Gtk.Label(language['Name'],name ="language-label")
            language['Button'] = Gtk.RadioButton.new_with_label_from_widget(self.group,"")
            if self.current_lang == language['Lang']:
                language['Button'].set_active(True)
            language['Button'].connect("toggled",self.radioButtonSelected, language['Lang'])
            languageBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            f = Gtk.Frame()
            languageBox.pack_start(languageImage, False, True, 5)
            languageBox.pack_end(language['Button'], False, False, 5)
            languageBox.pack_end(languageName, True, True, 5)
            languageBox.set_size_request(50, 50)
            eventBox = Gtk.EventBox()
            eventBox.connect("button-press-event", self.eventBoxLanguage, language['Lang'])
            eventBox.add(languageBox)
            f.add(eventBox)
            grid.attach(f, count, row, 1, 1)
            count += 1
            if count % 2 == 0:
                count = 0
                row += 1
        gridBox = Gtk.Box()
        gridBox.set_halign(Gtk.Align.CENTER)
        gridBox.add(grid)
        self.continueButton = Gtk.Button(_('Continue'),name ="flat-button-blue")
        self.continueButton.connect("clicked", self.on_click_continue_button)
        
        self.continueButton.set_hexpand(True)
        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        buttonBox.pack_start(self.continueButton, False, False, 0)
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.pack_start(initHeader, True, True, 0)
        main.pack_end(buttonBox, True, True, 20)
        main.pack_end(gridBox, True, True, 20)

        self.content.add(main)
        self._screen.base_panel.visible_menu(False)
    def on_click_continue_button(self, continueButton):
        if self.lang_changed:
            self._screen.change_language(self.new_lang)
            self._screen.restart_ks()
        else:
            self._screen.show_panel("co_print_contract_approval", "co_print_contract_approval", None, 1, True)

        
    def radioButtonSelected(self, button, lang):
        if lang != self.current_lang: 
            self.new_lang = lang
            self.lang_changed = True
        else:
            self.lang_changed = False
    
    def eventBoxLanguage(self, button, gparam, lang):
            for language in self.languages:
                if lang != language['Lang']:
                    language['Button'].set_active(False)
                else:
                    language['Button'].set_active(True)