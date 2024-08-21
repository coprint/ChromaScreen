import pyudev
from gi.repository import Gtk, GLib
from ks_includes.screen_panel import ScreenPanel
class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        spinner = Gtk.Spinner()
        spinner.props.width_request = 200 
        spinner.props.height_request = 300
        spinner.start()
        stepLabel = Gtk.Label(_("Reading the head connection.."), name="test-green-label")
        testLabel = Gtk.Label(_("Connecting to head"), name="test-header-white-label")
        testBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        testBox.set_valign(Gtk.Align.CENTER)
        testBox.pack_start(spinner, False, False, 0)
        testBox.pack_start(stepLabel, False, False, 0)
        testBox.pack_start(testLabel, False, False, 0)
        #----------Main-Box--------
        main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main.pack_start(testBox, True, True, 0)
        main.set_halign(Gtk.Align.CENTER)
        main.set_valign(Gtk.Align.CENTER)
        self.content.add(main)
        GLib.timeout_add_seconds(1, self.control_usb,None)

    def control_usb(self, args):
        self.isSuccess= False
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb')
        device = monitor.poll(timeout=10)
        if device != None:
            if device.action == 'add':
                self._screen._ws.klippy.restart_firmware()
                GLib.timeout_add_seconds(10, self.on_click_continue_button,)
                self.isSuccess= True
            if device.action == 'unbind':
                print('{} unbind'.format(device))
        if self.isSuccess  == False:
            GLib.timeout_add_seconds(1, self.control_usb, None)
        return False

    def on_click_continue_button(self):
        self._screen.show_panel("co_print_test_main_fan", "co_print_test_main_fan", None, 1,True)

