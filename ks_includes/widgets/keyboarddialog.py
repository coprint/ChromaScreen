import logging
import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
class KeyboardDialog(Gtk.Dialog):
    langs = ["de", "en", "fr", "es"]
    def __init__(self, screen, close_cb, entry=None):
        super().__init__(title="My Dialog",parent=None ,flags=0)
        self.set_default_size(600, 200)
        pos = self.get_position()
        self.move(pos[0]+ 5, pos[1] + 325)
        self.close_cb = close_cb
        self.keyboard = Gtk.Grid()
        self.keyboard.set_direction(Gtk.TextDirection.LTR)
        self.timeout = self.clear_timeout = None
        self.entry = entry
        language = self.detect_language(screen._config.get_main_config().get("language", None))
        logging.info(f"Keyboard {language}")
        if language == "de":
            self.keys = [
                [
                    ["q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "ü", "⌫"],
                    ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ö", "ä"],
                    ["ABC", "123", "#+=", "y", "x", "c", "v", "b", "n", "m"],
                ],
                [
                    ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P", "Ü", "⌫"],
                    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ö", "Ä"],
                    ["abc", "123", "#+=", "Y", "X", "C", "V", "B", "N", "M"],
                ],
                [
                    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "ß", "⌫"],
                    ["-", "/", ":", ";", "(", ")", "$", "&", "@", "\"", "ẞ"],
                    ["ABC", "abc", "#+=", ".", ",", "?", "!", "'"],
                ],
                [
                    ["[", "]", "{", "}", "#", "%", "^", "*", "+", "=", "⌫"],
                    ["_", "\\", "|", "~", "<", ">", "€", "£", "¥", "•"],
                    ["ABC", "abc", "123", ".", ",", "?", "!", "'"],
                ]
            ]
        elif language == "fr":
            self.keys = [
                [
                    ["a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "⌫"],
                    ["q", "s", "d", "f", "g", "h", "j", "k", "l", "m"],
                    ["ABC", "123", "#+=", "w", "x", "c", "v", "b", "n"],
                ],
                [
                    ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "⌫"],
                    ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
                    ["abc", "123", "#+=", "W", "X", "C", "V", "B", "N"],
                ],
                [
                    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "⌫"],
                    ["-", "/", ":", ";", "(", ")", "$", "&", "@", "\""],
                    ["ABC", "abc", "#+=", ".", ",", "?", "!", "'"],
                ],
                [
                    ["[", "]", "{", "}", "#", "%", "^", "*", "+", "=", "⌫"],
                    ["_", "\\", "|", "~", "<", ">", "€", "£", "¥", "•"],
                    ["ABC", "abc", "123", ".", ",", "?", "!", "'"],
                ]
            ]
        else:
            self.keys = [
                [
                    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                    ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
                    ["⇧", "z", "x", "c", "v", "b", "n", "m", ".","⌫"],
                ],
                [
                    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
                    ["⬆", "Z", "X", "C", "V", "B", "N", "M", ".","⌫"],
                ],
                [
                    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                    ["-", "/", ":", ";", "(", ")", "$", "&", "@", "\""],
                    ["#+=", ".", ",", "?", "!", "'", "⌫"],
                ],
                [
                    ["[", "]", "{", "}", "#", "%", "^", "*", "+", "="],
                    ["_", "\\", "|", "~", "<", ">", "€", "£", "¥", "•"],
                    ["123", ".", ",", "?", "!", "'", "⌫"],
                ]
            ]
        for pallet in self.keys:
            pallet.append(["✕","123", " ", "✔", "ABC"])
        self.buttons = self.keys.copy()
        for p, pallet in enumerate(self.keys):
            for r, row in enumerate(pallet):
                for k, key in enumerate(row):
                    if key == "⌫":
                        self.buttons[p][r][k] = screen.gtk.Button("backspace", scale=.6)
                    elif key == "✕":
                        self.buttons[p][r][k] = screen.gtk.Button("cancel", scale=.6)
                    elif key == "✔":
                        self.buttons[p][r][k] = screen.gtk.Button("complete", scale=.6)
                    else:
                        self.buttons[p][r][k] = screen.gtk.Button(label=key, lines=1)
                    self.buttons[p][r][k].set_hexpand(True)
                    self.buttons[p][r][k].set_vexpand(True)
                    self.buttons[p][r][k].connect('button-press-event', self.repeat, key)
                    self.buttons[p][r][k].connect('button-release-event', self.release)
                    if key == "⇧" or key =="⬆" or key == "⌫":
                        self.buttons[p][r][k].get_style_context().add_class("keyboard_pad_special")
                    else:
                        self.buttons[p][r][k].get_style_context().add_class("keyboard_pad")
        self.pallet_nr = 0
        self.set_pallet(self.pallet_nr)
        box = self.get_content_area()
        box.add(self.keyboard)
        self.show_all()

    def detect_language(self, language):
        if language is None or language == "system_lang":
            for language in self.langs:
                if os.getenv('LANG').lower().startswith(language):
                    return language
        for _ in self.langs:
            if language.startswith(_):
                return _
        return "en"

    def set_pallet(self, p):
        for _ in range(len(self.keys[self.pallet_nr]) + 1):
            self.keyboard.remove_row(0)
        self.pallet_nr = p
        for r, row in enumerate(self.keys[p][:-1]):
            for k, key in enumerate(row):
                if p == 1 or p == 0:
                    x = k * 2 +1 if r == 1 else k * 2
                else:
                    x = k * 2  if r == 1 else k * 2
                self.keyboard.attach(self.buttons[p][r][k], x, r, 2, 1)
        self.keyboard.attach(self.buttons[p][3][0], 0, 4, 2, 1)  # ✕
        if p == 1 or p ==0:
            self.keyboard.attach(self.buttons[p][3][1], 2, 4, 2, 1)  # ABC
        else:
            self.keyboard.attach(self.buttons[p][3][4], 2, 4, 2, 1)  # ABC
        self.keyboard.attach(self.buttons[p][3][2], 4, 4, 14, 1)  # Space
        self.keyboard.attach(self.buttons[p][3][3], 18, 4, 2, 1)  # ✔
        self.show_all()

    def repeat(self, widget, event, key):
        # Button-press
        self.update_entry(widget, key)
        if self.timeout is None and key == "⌫":
            # Hold for repeat, hold longer to clear the field
            self.clear_timeout = GLib.timeout_add_seconds(3, self.clear, widget)
            # This can be used to repeat all the keys,
            # but I don't find it useful on the console
            self.timeout = GLib.timeout_add(400, self.repeat, widget, None, key)
        return True

    def release(self, widget, event):
        # Button-release
        if self.timeout is not None:
            GLib.source_remove(self.timeout)
            self.timeout = None
        if self.clear_timeout is not None:
            GLib.source_remove(self.clear_timeout)
            self.clear_timeout = None

    def clear(self, widget=None):
        self.entry.set_text("")
        if self.clear_timeout is not None:
            GLib.source_remove(self.clear_timeout)
            self.clear_timeout = None

    def update_entry(self, widget, key):
        if key == "⌫":
            Gtk.Entry.do_backspace(self.entry)
        elif key == "✔":
            self.close_cb()
            return
        elif key == "✕":
            self.clear()
            self.close_cb()
            return
        elif key == "⬆":
            self.set_pallet(0)
        elif key == "ABC":
            self.set_pallet(0)
        elif key == "⇧":
            self.set_pallet(1)
        elif key == "123":
            self.set_pallet(2)
        elif key == "#+=":
            self.set_pallet(3)
        else:
            Gtk.Entry.do_insert_at_cursor(self.entry, key)