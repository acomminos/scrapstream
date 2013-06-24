#!/usr/bin/env python
#
# Copyright (C) 2012 Andrew Comminos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, WebKit2
from threading import Timer
from stream_manager import StreamManager
from stream_settings import StreamSettings

ALPHA_TEXT = "<h1>Scrapstream Alpha</h1>Scrapstream is in alpha right now.<br>Don't use this for professional streami    ng!<br><br>Enjoy!<br>- Andrew (Morlunk)"

class StreamWindow(object):

    def __init__(self):
        handlers = {
            "onLiveActivate": self.stream,
            "onCancelActivate": self.quit,
            "save-settings": self.save_settings,
            "delete-event": self.quit
        }

        builder = Gtk.Builder()
        builder.add_from_file("xml/stream_dialog.glade")
        self.dialog = builder.get_object("dialog1")
        self.username_entry = builder.get_object("username_entry")
        self.stream_key_entry = builder.get_object("stream_key_entry")
        self.remember_me = builder.get_object("remember_box")
        self.stream_button = builder.get_object("stream_button")

        # Settings
        self.options_notebook = builder.get_object("options_notebook")
        self.custom_audio = builder.get_object("audio_usecustom")
        self.custom_audio_file = builder.get_object("audio_filechooser")
        self.framerate_scale = builder.get_object("framerate_scale")
        self.fps_adjustment = builder.get_object("fps_adjustment")
        self.output_width = builder.get_object("output_width")
        self.output_height = builder.get_object("output_height")
        self.capture_x = builder.get_object("capture_x")
        self.capture_y = builder.get_object("capture_y")
        self.capture_width = builder.get_object("capture_width")
        self.capture_height = builder.get_object("capture_height")

        self.load_settings()

        # Show stream in WebKit frame
        frame = builder.get_object('web_box')
        self.webview = WebKit2.WebView()
        self.webview.set_hexpand(True)
        self.webview.set_vexpand(True)
        self.webview.load_html(ALPHA_TEXT, "")
        frame.add(self.webview)

        builder.connect_signals(handlers)

        # Monitor for vlc and jtvlc process changes
        manager = StreamManager.get_stream_manager()
        manager.subscribe(self.stream_update)
    
    def load_settings(self):
        self.username_entry.set_text(StreamSettings.username)
        self.stream_key_entry.set_text(StreamSettings.stream_key)
        self.remember_me.set_active(StreamSettings.remember_me)
        self.fps_adjustment.set_value(StreamSettings.frame_rate)
        self.output_width.set_text("%d" % StreamSettings.output_width)
        self.output_height.set_text("%d" % StreamSettings.output_height)
        self.capture_x.set_text("%d" % StreamSettings.capture_x)
        self.capture_y.set_text("%d" % StreamSettings.capture_y)
        self.capture_width.set_text("%d" % StreamSettings.capture_width)
        self.capture_height.set_text("%d" % StreamSettings.capture_height)
        self.custom_audio.set_active(StreamSettings.custom_audio)
        self.custom_audio_file.set_filename(StreamSettings.audio_file)

    def save_settings(self, widget=None, userdata=None):
        """Saves settings changed in this window to the StreamSettings module, followed by a commit to the config file."""
        StreamSettings.username = self.username_entry.get_text()
        StreamSettings.remember_me = self.remember_me.get_active()
        StreamSettings.stream_key = self.stream_key_entry.get_text()
        StreamSettings.frame_rate = self.fps_adjustment.get_value()
        StreamSettings.output_width = int(self.output_width.get_text())
        StreamSettings.output_height = int(self.output_height.get_text())
        StreamSettings.capture_x = int(self.capture_x.get_text())
        StreamSettings.capture_y = int(self.capture_y.get_text())
        StreamSettings.capture_width = int(self.capture_width.get_text())
        StreamSettings.capture_height = int(self.capture_height.get_text())
        StreamSettings.custom_audio = self.custom_audio.get_active()
        StreamSettings.audio_file = self.custom_audio_file.get_filename()
        StreamSettings.save()


    def show(self):
        self.dialog.show_all()

    def stream(self, button, userdata=None):
        if StreamManager.get_stream_manager().is_running() is False:
            self.start_stream()
        else:
            self.stop_stream()

    def start_stream(self):
        StreamManager.get_stream_manager().start()
        self.webview.load_uri("http://twitch.tv/%s/popout" % self.username_entry.get_text())

    def stop_stream(self):
        StreamManager.get_stream_manager().stop()

    def stream_update(self, stream_manager):
        if stream_manager.is_running():
            self.stream_button.set_label("Stop")
            self.options_notebook.set_sensitive(False)
        else:
            self.stream_button.set_label("Go Live!")
            self.options_notebook.set_sensitive(True)

    def quit(self, button, userdata=None):
        self.dialog.hide()
        Gtk.main_quit()
        manager = StreamManager.get_stream_manager()
        manager.stop()
