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
import stream_settings

ALPHA_TEXT = "<h1>Scrapstream Alpha</h1>Scrapstream is in alpha right now.<br>Don't use this for professional streaming!<br><br>Enjoy!<br>- Andrew (Morlunk)"

class StreamWindow(object):

    def __init__(self):
        handlers = {
            "onLiveActivate": self.stream,
            "onCancelActivate": self.quit,
            "audio-source-changed": self.audio_source_changed,
            "save-settings": self.save_settings,
            "delete-event": self.quit,
            "overlay-add": self.overlay_add,
            "overlay-delete": self.overlay_delete,
            "save-overlay-dialog": self.save_overlay_dialog,
            "hide-overlay-dialog": self.hide_overlay_dialog
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
        self.framerate_scale = builder.get_object("framerate_scale")
        self.fps_adjustment = builder.get_object("fps_adjustment")
        self.output_width = builder.get_object("output_width")
        self.output_height = builder.get_object("output_height")
        self.capture_x = builder.get_object("capture_x")
        self.capture_y = builder.get_object("capture_y")
        self.capture_width = builder.get_object("capture_width")
        self.capture_height = builder.get_object("capture_height")

        # Audio
        self.audio_source_box = builder.get_object("audio_source_box")
        self.audio_youtube_url = builder.get_object("audio_youtube_url")
        self.audio_custom_file = builder.get_object("audio_filechooser")

        # Overlay
        self.overlay_dialog = builder.get_object("overlay_dialog")
        self.overlay_dialog_image = builder.get_object("overlay_dialog_image")
        self.overlay_dialog_x = builder.get_object("overlay_dialog_x")
        self.overlay_dialog_y = builder.get_object("overlay_dialog_y")
        self.overlay_dialog_anchor = builder.get_object("overlay_dialog_anchor")
        self.overlay_store = builder.get_object("overlay_store")
        self.overlay_selection = builder.get_object("overlay_selection")

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
        config = stream_settings.get_config()
        self.username_entry.set_text(config['username'])
        self.stream_key_entry.set_text(config['stream_key'])
        self.remember_me.set_active(config['remember_me'])
        self.fps_adjustment.set_value(config['frame_rate'])
        self.output_width.set_text(str(config['output_width']))
        self.output_height.set_text(str(config['output_height']))
        self.capture_x.set_text(str(config['capture_x']))
        self.capture_y.set_text(str(config['capture_y']))
        self.capture_width.set_text(str(config['capture_width']))
        self.capture_height.set_text(str(config['capture_height']))
        self.audio_source_box.set_active_id(config['audio_source_id'])
        self.audio_youtube_url.set_text(config['audio_youtube_url'])
        self.audio_custom_file.set_filename(config['audio_file'])

        # Add overlay items
        for overlay in config['overlays']:
            self.overlay_store.append([overlay['file'], overlay['x'], overlay['y'], overlay['gravity']])

    def save_settings(self, widget=None, userdata=None):
        """Saves settings changed in this window to the stream_settings module, followed by a commit to the config file."""
        config = stream_settings.get_config()
        config['remember_me'] = self.remember_me.get_active()
        if self.remember_me.get_active():
            config['username'] = self.username_entry.get_text()
            config['stream_key'] = self.stream_key_entry.get_text()
        config['frame_rate'] = self.fps_adjustment.get_value()
        config['output_width'] = self.output_width.get_text()
        config['output_height'] = self.output_height.get_text()
        config['capture_x'] = self.capture_x.get_text()
        config['capture_y'] = self.capture_y.get_text()
        config['capture_width'] = self.capture_width.get_text()
        config['capture_height'] = self.capture_height.get_text()
        config['audio_file'] = self.audio_custom_file.get_filename()
        config['audio_youtube_url'] = self.audio_youtube_url.get_text()
        config['audio_source_id'] = self.audio_source_box.get_active_id()

        config['overlays'] = []
        # Save overlay items
        for overlay_row in self.overlay_store:
            overlay = {'file': overlay_row[0],
                       'x': overlay_row[1],
                       'y': overlay_row[2],
                       'gravity': overlay_row[3]}
            config['overlays'].append(overlay)

        stream_settings.save()


    def show(self):
        self.dialog.show_all()

    def stream(self, button, userdata=None):
        if StreamManager.get_stream_manager().is_running() is False:
            self.start_stream()
        else:
            self.stop_stream()

    def start_stream(self):
        StreamManager.get_stream_manager().start()
        if self.webview.get_uri() != ("http://www.twitch.tv/%s" % self.username_entry.get_text()):
            self.webview.load_uri("http://www.twitch.tv/%s" % self.username_entry.get_text())

    def stop_stream(self):
        StreamManager.get_stream_manager().stop()

    def stream_update(self, stream_manager):
        if stream_manager.is_running():
            self.stream_button.set_label("Stop")
        else:
            self.stream_button.set_label("Go Live!")

    def audio_source_changed(self, combobox, userdata=None):
        print("todo")
        # TODO:
        # - Use YouTube API to stream a mp4/flv into the ffmpeg instance.
        # - Store audio source selected in settings.
        # - Hide other audio fields when a different combo item is visible

    def overlay_add(self, button, userdata=None):
        self.overlay_dialog.show()

    def overlay_delete(self, button, userdata=None):
        self.overlay_store.remove(self.overlay_selection.get_selected()[1])

    def save_overlay_dialog(self, widget, userdata=None):
        overlay = [
                self.overlay_dialog_image.get_filename(),
                int(self.overlay_dialog_x.get_text()),
                int(self.overlay_dialog_y.get_text()),
                self.overlay_dialog_anchor.get_active_id()]
        self.overlay_store.append(overlay)
        self.overlay_dialog.hide()

    def hide_overlay_dialog(self, widget, userdata=None):
        self.overlay_dialog.hide()

    def quit(self, button, userdata=None):
        self.dialog.hide()
        Gtk.main_quit()
        manager = StreamManager.get_stream_manager()
        manager.unsubscribe(self.stream_update)
        if manager.is_running():
            manager.stop()
