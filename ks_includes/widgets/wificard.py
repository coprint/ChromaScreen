import subprocess
import gi
import numpy as np
from ks_includes.widgets.infodialog import InfoDialog
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
class WifiCard(Gtk.Box):
    def __init__(self, this, _image, _wifiName, _connectStatus, _connectionButtonVisible = False):
        super().__init__()
        self.parent = this
        image = this._gtk.Image(_image, this._gtk.content_width * .08 , this._gtk.content_height * .08)
        self.disconnectNetworkButton = Gtk.Button(_('Disconnect'),name ="disconnect-network-button")
        self.disconnectNetworkButton.connect("clicked", self.disconnect_network, _wifiName)
        disconnectNetworkButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        disconnectNetworkButtonBox.set_valign(Gtk.Align.CENTER)
        disconnectNetworkButtonBox.pack_start(self.disconnectNetworkButton, False, False, 0)

        self.forgetNetworkButton = Gtk.Button(_('Forget Network'),name ="forgot-network-button")
        self.forgetNetworkButton.connect("clicked", self.remove_network, _wifiName)
        forgetNetworkButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        forgetNetworkButtonBox.set_valign(Gtk.Align.CENTER)
        forgetNetworkButtonBox.pack_start(self.forgetNetworkButton, False, False, 0)
        
        wifiNameLabel = Gtk.Label(self.rename_string(_wifiName,30), name="wifi-name-label")
        wifiNameLabel.set_justify(Gtk.Justification.LEFT)
        wifiNameLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        wifiNameLabelBox.pack_start(wifiNameLabel, False, False, 0)
        
        connectStatusLabel = Gtk.Label(_connectStatus, name ="wifi-status-label")
        connectStatusLabel.set_justify(Gtk.Justification.LEFT)
        connectStatusLabelBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        connectStatusLabelBox.pack_start(connectStatusLabel, False, False, 0)
        
        wifiLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        wifiLabelBox.pack_start(wifiNameLabelBox, False, False, 0)
        wifiLabelBox.pack_start(connectStatusLabelBox, False, False, 0)

        wifiCardBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        wifi_list_string = subprocess.check_output(['nmcli', '-f', 'NAME', 'con', 'show']).decode()
        wifi_list = wifi_list_string.split("\n")
        self.is_saved = np.any([_wifiName == i.strip() for i in wifi_list])
        if _connectionButtonVisible == True:
            wifiCardBox.set_name("wifi-card-box")
            wifiCardBox.pack_start(wifiLabelBox, False, False, 0)
            wifiCardBox.pack_end(image, False, False, 20)
            wifiCardBox.pack_end(disconnectNetworkButtonBox, False, False, 0)
            if   self.is_saved:
                wifiCardBox.pack_end(forgetNetworkButtonBox, False, False, 0)
        else:
            wifiCardBox.set_name("wifi-card-box")
            wifiCardBox.pack_start(wifiLabelBox, False, False, 0)
            wifiCardBox.pack_end(image, False, False, 20)
            if self.is_saved:
                wifiCardBox.pack_end(forgetNetworkButtonBox, False, False, 0)
        cartesianTypeEventBox = Gtk.EventBox()
        cartesianTypeEventBox.connect("button-press-event", this.wifiChanged, _wifiName)
        cartesianTypeEventBox.add(wifiCardBox)
        self.add(cartesianTypeEventBox)

    def rename_string(self, string, length_string):
        if len(string) > length_string:
            res = []
            #return string[:length_string-3] + "..."
            for id in range(0, len(string)):
                if id % length_string == 0 and id != 0:
                    res.append('\n')
                res.append(string[id])
            return ''.join(res)
        else:
            return string
        
    def execute_command(self, name):
        process = subprocess.run(['nmcli', 'con', 'down', 'id', name], stdout=subprocess.PIPE)
        self.parent.refresh(None)
        self.waitDialog.response(Gtk.ResponseType.CANCEL)
        self.waitDialog.destroy()  

    def disconnect_network(self, widget, name):
        GLib.idle_add(self.execute_command, name)  
        self.waitDialog = InfoDialog(self, _("Please Wait"), True)
        self.waitDialog.get_style_context().add_class("alert-info-dialog")
        self.waitDialog.set_decorated(False)
        self.waitDialog.set_size_request(0, 0)
        response = self.waitDialog.run()

    def execute_command_remove(self, name):
        process = subprocess.run(['nmcli', 'connection', 'delete', name], stdout=subprocess.PIPE)
        self.parent.refresh(None)
        self.waitDialog.response(Gtk.ResponseType.CANCEL)
        self.waitDialog.destroy()  

    def remove_network(self, widget, name):
        GLib.idle_add(self.execute_command_remove, name)  
        self.waitDialog = InfoDialog(self, _("Please Wait"), True)
        self.waitDialog.get_style_context().add_class("alert-info-dialog")
        self.waitDialog.set_decorated(False)
        self.waitDialog.set_size_request(0, 0)
        response = self.waitDialog.run()