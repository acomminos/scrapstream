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
from settings_window import SettingsWindow

ALPHA_TEXT = "<h1>Scrapstream Alpha</h1>Scrapstream is in alpha right now.<br>Don't use this for professional streami    ng!<br><br>Enjoy!<br>- Andrew (Morlunk)"

class StreamWindow(object):

    def __init__(self):
        handlers = {
            "onLiveActivate": self.stream,
            "onSettingsActivate": self.settings,
            "onCancelActivate": self.quit,
            "rememberToggle": self.remember_me,
            "custom-audio-set": self.custom_audio_set,
            "audio-file-set": self.audio_file_set,
            "delete-event": self.quit
        }

        builder = Gtk.Builder()
        builder.add_from_file("xml/stream_dialog.glade")
        self.dialog = builder.get_object("dialog1")
        self.username_entry = builder.get_object("username_entry")
        self.username_entry.set_text(StreamSettings.username)
        self.stream_key_entry = builder.get_object("stream_key_entry")
        self.stream_key_entry.set_text(StreamSettings.stream_key)
        self.remember_me = builder.get_object("remember_box")
        self.remember_me.set_active(StreamSettings.remember_me)
        self.settings_button = builder.get_object("settings_button")
        self.stream_button = builder.get_object("stream_button")

        self.custom_audio = builder.get_object("audio_usecustom")
        self.custom_audio.set_active(StreamSettings.custom_audio)
        self.custom_audio_file = builder.get_object("audio_filechooser")
        self.custom_audio_file.set_filename(StreamSettings.audio_file)

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

    def show(self):
        self.dialog.show_all()

    def stream(self, button, userdata=None):
        if StreamManager.get_stream_manager().is_streaming() is False:
            self.start_stream()
        else:
            self.stop_stream()

    def settings(self, button, userdata=None):
        settings = SettingsWindow()
        settings.show()

    def start_stream(self):
        StreamSettings.username = self.username_entry.get_text()
        StreamSettings.stream_key = self.stream_key_entry.get_text()
        StreamSettings.save()

        StreamManager.get_stream_manager().start_streaming()
        self.settings_button.set_sensitive(False)
        self.stream_button.set_label("Stop")
        self.webview.load_uri("http://twitch.tv/%s/popout" % self.username_entry.get_text())

    def stop_stream(self):
        StreamManager.get_stream_manager().stop_streaming()
        self.settings_button.set_sensitive(True)
        self.stream_button.set_label("Go Live!")

    def stream_update(self, stream_manager):
        if stream_manager.streaming:
            self.settings_button.set_sensitive(False)
            self.stream_button.set_label("Stop")
        else:
            self.settings_button.set_sensitive(True)
            self.stream_button.set_label("Go Live!")

    def remember_me(self, checkbox, userdata=None):
        """ Called when the 'Remember Me' checkbox is pressed. """
        StreamSettings.remember_me = checkbox.get_active()
        StreamSettings.save()

    def custom_audio_set(self, widget, userdata=None):
        StreamSettings.custom_audio = widget.get_active()
        StreamSettings.save()

    def audio_file_set(self, widget, userdata=None):
        StreamSettings.audio_file = widget.get_filename()
        StreamSettings.save()

    def quit(self, button, userdata=None):
        self.dialog.hide()
        Gtk.main_quit()
        manager = StreamManager.get_stream_manager()
        manager.shutdown()
