import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
class Timezone(Gtk.Box):
    def __init__(self, this, _offset, _current_time, oset):
        super().__init__()
        timezoneLabel = Gtk.Label(_offset + " Time Zone", name="timezone-label")
        timezoneLabel.set_justify(Gtk.Justification.LEFT)
        timeLabel = Gtk.Label(_current_time, name="time-label")
        timezoneLabel.set_justify(Gtk.Justification.RIGHT)
        timezoneBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        timezoneBox.set_name("timezone-box")
        timezoneBox.pack_start(timezoneLabel, False, False, 0)
        timezoneBox.pack_end(timeLabel, False, False, 0)
        mainEventBox = Gtk.EventBox()
        mainEventBox.connect("button-press-event", this.timezone_select, oset, _current_time)
        mainEventBox.add(timezoneBox)
        self.add(mainEventBox)