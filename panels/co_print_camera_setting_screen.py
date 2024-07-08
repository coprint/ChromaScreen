import logging
import os
from ks_includes.widgets.checkbuttonbox import CheckButtonBox
import gi
import contextlib
from ks_includes.widgets.bottommenu import BottomMenu
from ks_includes.widgets.addnetworkdialog import AddNetworkDialog
from ks_includes.widgets.infodialog import InfoDialog
from ks_includes.widgets.wificard import WifiCard
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GLib, Gdk, GdkPixbuf

from ks_includes.screen_panel import ScreenPanel
from contextlib import suppress
import mpv
def create_panel(*args):
    return CoPrintCameraSettingScreen(*args)


class CoPrintCameraSettingScreen(ScreenPanel):

# class Panel(ScreenPanel):
    def __init__(self, screen, title):
        super().__init__(screen, title)
        
        menu = BottomMenu(self, False)
        self.dialog = None
        
        cameraTitle = Gtk.Label(_("Printing Camera"), name="printer-type-title-label")
        cameraTitle.set_justify(Gtk.Justification.CENTER)
        self.cameraTitleBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.cameraTitleBox.set_halign(Gtk.Align.CENTER)
        self.cameraTitleBox.pack_start(cameraTitle, False, False, 0)
        
        cameraContent = Gtk.Label(_("Please connect a camera using the USB ports for printing monitoring."), name="printer-type-content-label")
        cameraContent.set_max_width_chars(60)
        cameraContent.set_line_wrap(True)
        cameraContent.set_justify(Gtk.Justification.CENTER)
        self.cameraContentBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.cameraContentBox.set_halign(Gtk.Align.CENTER)
        self.cameraContentBox.pack_start(cameraContent, False, False, 0)
        
        cameraLabelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        cameraLabelBox.set_valign(Gtk.Align.CENTER)
        cameraLabelBox.set_halign(Gtk.Align.CENTER)
        cameraLabelBox.set_hexpand(True)
        cameraLabelBox.pack_start(self.cameraTitleBox, False, False, 0)
        cameraLabelBox.pack_end(self.cameraContentBox, False, False, 10)
        


        self.cameraBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.cameraBox.set_name("camera-box")
        cameraLabel = Gtk.Label(_("No Camera"), name="camera-label")
        cameraImage = self._gtk.Image("no-camera", self._screen.width *.07, self._screen.width *.07)
       
        #self.cameraBox.pack_end(cameraImage, False, False, 0)
        
        camera_enable = False
        self.mpv = None
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        for i, cam in enumerate(self._printer.cameras):
            if not cam["enabled"]:
                continue
            #logging.info(cam)
            cam[cam["name"]] = self._gtk.Button(
                image_name="camera", label=cam["name"],
                scale=self.bts, position=Gtk.PositionType.LEFT, lines=1
            )
            cam[cam["name"]].set_hexpand(True)
            cam[cam["name"]].set_vexpand(True)
            cam[cam["name"]].connect("clicked", self.play, cam)
            camera_enable = True
            self.cameraBox.pack_end(cam[cam["name"]], False, False, 0)

        if camera_enable == False:
            self.cameraBox.pack_start(cameraLabel, False, False, 0)
        self.scroll = self._gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.add(box)


        self.refreshIcon = self._gtk.Image("update", self._screen.width *.035, self._screen.width *.035)
        refreshButton = Gtk.Button(name ="setting-button")
        refreshButton.set_image(self.refreshIcon)
        refreshButton.set_always_show_image(True)
        refreshButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        refreshButtonBox.set_valign(Gtk.Align.CENTER)
        refreshButtonBox.add(refreshButton)

        self.fullScreenIcon = self._gtk.Image("full_screen", self._screen.width * .035, self._screen.width * .035)
        fullScreenButton = Gtk.Button(name="setting-button")
        fullScreenButton.set_image(self.fullScreenIcon)
        fullScreenButton.set_always_show_image(True)
        fullScreenButtonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        fullScreenButtonBox.set_valign(Gtk.Align.CENTER)
        fullScreenButtonBox.add(fullScreenButton)
        
        cameraRefreshBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        cameraRefreshBox.pack_start(fullScreenButtonBox, False, False, 0)
        cameraRefreshBox.pack_start(self.cameraBox, False, False, 0)

        cameraRefreshBox.pack_end(refreshButtonBox, False, False, 0)
        
        recordIcon = self._gtk.Image("image", self._screen.width *.05, self._screen.width *.05)
        recordLabel = Gtk.Label(_("Records"))
        recordButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        recordButtonBox.set_halign(Gtk.Align.CENTER)
        recordButtonBox.set_valign(Gtk.Align.CENTER)
        recordButtonBox.pack_start(recordIcon, False, False, 0)
        recordButtonBox.pack_start(recordLabel, False, False, 0)
        recordButton = Gtk.Button(name ="camera-button")
        recordButton.set_always_show_image(True)
        recordButton.add(recordButtonBox)
        
        camSettingsIcon = self._gtk.Image("support", self._screen.width *.05, self._screen.width *.05)
        camSettingsLabel = Gtk.Label(_("Cam Settings"))
        camSettingsButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        camSettingsButtonBox.set_halign(Gtk.Align.CENTER)
        camSettingsButtonBox.set_valign(Gtk.Align.CENTER)
        camSettingsButtonBox.pack_start(camSettingsIcon, False, False, 0)
        camSettingsButtonBox.pack_start(camSettingsLabel, False, False, 0)
        camSettingsButton = Gtk.Button(name ="camera-button")
        camSettingsButton.set_always_show_image(True)
        camSettingsButton.add(camSettingsButtonBox)
        
        cameraButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        cameraButtonBox.set_halign(Gtk.Align.CENTER)
        cameraButtonBox.set_valign(Gtk.Align.CENTER)
        cameraButtonBox.pack_start(recordButton, False, False, 0)
        cameraButtonBox.pack_start(camSettingsButton, False, False, 0)
        
        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        main.set_hexpand(True)
        main.set_halign(Gtk.Align.CENTER)
        main.pack_start(cameraRefreshBox, False, False, 50)
        


      
        #self.content.add(self.scroll)


        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        page.set_vexpand(True)
        page.pack_start(cameraLabelBox, False, False, 0)
        page.pack_start(main, True, True, 0)
        page.pack_end(menu, False, True, 0)
        page.pack_start(cameraButtonBox, False, False, 0)
        
        self.content.add(page)
        self.open_info_dialog()
        #GLib.idle_add(self.show_frame, None)


    def play(self, widget, cam):
        url = cam['stream_url']
        if url.startswith('/'):
            logging.info("camera URL is relative")
            endpoint = self._screen.apiclient.endpoint.split(':')
            url = f"{endpoint[0]}:{endpoint[1]}{url}"
        if '/webrtc' in url:
            self._screen.show_popup_message(_('WebRTC is not supported by the backend trying Stream'))
            url = url.replace('/webrtc', '/stream')
        vf = ""
        if cam["flip_horizontal"]:
            vf += "hflip,"
        if cam["flip_vertical"]:
            vf += "vflip,"
        vf += f"rotate:{cam['rotation'] * 3.14159 / 180}"
        logging.info(f"video filters: {vf}")

        if self.mpv:
            self.mpv.terminate()
        self.mpv = mpv.MPV(fullscreen=False, log_handler=self.log, vo='gpu,wlshm,xv,x11')

        self.mpv.vf = vf

        with suppress(Exception):
            self.mpv.profile = 'sw-fast'

        # LOW LATENCY PLAYBACK
        with suppress(Exception):
            self.mpv.profile = 'low-latency'
        self.mpv.untimed = True
        self.mpv.audio = 'no'

        @self.mpv.on_key_press('MBTN_LEFT' or 'MBTN_LEFT_DBL')
        def clicked():
            self.mpv.quit(0)

        logging.debug(f"Camera URL: {url}")
        self.mpv.play(url)

        try:
            self.mpv.wait_for_playback()
        except mpv.ShutdownError:
            logging.info('Exiting Fullscreen')
        except Exception as e:
            logging.exception(e)
        self.mpv.terminate()
        self.mpv = None
        if len(self._printer.cameras) == 1:
            self._screen._menu_go_back()

    def log(self, loglevel, component, message):
        logging.debug(f'[{loglevel}] {component}: {message}')
        if loglevel == 'error' and 'No Xvideo support found' not in message and 'youtube-dl' not in message:
            self._screen.show_popup_message(f'{message}')
   
    def show_frame(self, args):
        if self.mpv:
            self.mpv.terminate()
            self.mpv = None
            # Create mpv after show or the 'window' property will be None
        try:
            self.mpv = mpv.MPV(
                log_handler=self.log,
                vo=self.vo,
                profile='sw-fast',
            )
        except ValueError:
            self.mpv = mpv.MPV(
                log_handler=self.log,
                vo=self.vo,
            )
            # On wayland mpv cannot be embedded at least for now
            # https://github.com/mpv-player/mpv/issues/9654
            # if fs or self.wayland:
        self.mpv.fullscreen = True


        @self.mpv.on_key_press('MBTN_LEFT' or 'MBTN_LEFT_DBL')
        def clicked():
            self.mpv.quit(0)

        # else:
        #     self.mpv.wid = f'{self.da.get_property("window").get_xid()}'
        #
        #     @self.mpv.on_key_press('MBTN_LEFT' or 'MBTN_LEFT_DBL')
        #     def clicked():
        #         self._screen.show_popup_message(self.url, level=1)
        self.mpv.play(self.url)
        # if fs or self.wayland:
        try:
            self.mpv.wait_for_playback()
        except mpv.ShutdownError:
            logging.info('Exiting Fullscreen')
        except Exception as e:
            logging.exception(e)
        self.mpv.terminate()
        self.mpv = None
        self._screen._menu_go_back()

    def open_info_dialog(self):
        if self.dialog == None:
            self.dialog = InfoDialog(self, "Camera is not ready", False, True)
            self.dialog.get_style_context().add_class("alert-info-dialog")
        
            self.dialog.set_decorated(False)
            self.dialog.set_size_request(0, 0)
        
            response = self.dialog.run()
   
    def finished(self):
        
        self.dialog.response(Gtk.ResponseType.CANCEL)
        self.dialog.destroy()