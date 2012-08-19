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

from gi.repository import Gtk
from threading import Timer
from stream_manager import StreamManager
from stream_settings import StreamSettings

class StreamWindow(object):

    def __init__(self):
        handlers = {
            "onLiveActivate": self.stream,
            "onCancelActivate": self.quit,
            "rememberToggle": self.remember_me,
            "delete-event": self.quit
        }

        builder = Gtk.Builder()
        builder.add_from_file("xml/stream_dialog.glade")
        self.dialog = builder.get_object("dialog1")
        self.username_entry = builder.get_object("username_entry")
        self.username_entry.set_text(StreamSettings.stream_username)
        self.stream_key_entry = builder.get_object("stream_key_entry")
        self.stream_key_entry.set_text(StreamSettings.stream_key)
        self.remember_me = builder.get_object("remember_box")
        self.remember_me.set_active(StreamSettings.remember_me)
        self.stream_button = builder.get_object("stream_button")

        # Icons
        self.vlc_image = builder.get_object("vlc_image")
        self.jtvlc_image = builder.get_object("jtvlc_image")
        self.stream_image = builder.get_object("stream_image")

        # Status
        self.vlc_status = builder.get_object("vlc_status")
        self.jtvlc_status = builder.get_object("jtvlc_status")
        self.stream_status = builder.get_object("stream_status")

        self.vlc_running = False
        self.jtvlc_running = False
        self.stream_running = False

        # Progress
        self.stream_progress = builder.get_object("stream_progress")

        builder.connect_signals(handlers)

        # Monitor for vlc and jtvlc process changes
        manager = StreamManager.get_stream_manager()
        manager.subscribe(self.stream_update)

    def show(self):
        self.dialog.show_all()

    def stream_update(self, manager):
        progress = float(0)
        vlc_image = ""
        vlc_status = ""

        if manager.is_streaming() is False:
            self.stream_button.set_label("Go Live!")
        else:
            self.stream_button.set_label("Stop")

    
        if manager.is_vlc_running():
            vlc_image = "xml/res/vlc-active.png"
            vlc_status = "Online"
            progress += 1
        else:
            vlc_image = "xml/res/vlc-inactive.png"
            vlc_status = "Offline"

        if manager.is_vlc_running() != self.vlc_running:
            self.vlc_status.set_label(vlc_status)
            self.vlc_image.set_from_file(vlc_image)
            self.vlc_running = manager.is_vlc_running()

        jtvlc_image = ""
        jtvlc_status = ""

        if manager.is_jtvlc_running():
            jtvlc_image = "xml/res/jtv-active.png"
            jtvlc_status = "Online"
            progress += 1
        else:
            jtvlc_image = "xml/res/jtv-inactive.png"
            jtvlc_status = "Offline"
            
        if manager.is_jtvlc_running() != self.jtvlc_running:
            self.jtvlc_status.set_label(jtvlc_status)
            self.jtvlc_image.set_from_file(jtvlc_image)
            self.jtvlc_running = manager.is_jtvlc_running()

        stream_image = ""
        stream_status = ""

        if manager.is_vlc_running() and manager.is_jtvlc_running():
            stream_image = "xml/res/stream-active.png"
            stream_status = "Online"
            progress += 1
        else:
            stream_image = "xml/res/stream-inactive.png"
            stream_status = "Offline"

        if (manager.is_vlc_running() and manager.is_jtvlc_running()) != self.stream_running:
            self.stream_status.set_label(stream_status)
            self.stream_image.set_from_file(stream_image)
            self.stream_running = (manager.is_vlc_running() and manager.is_jtvlc_running())

        self.stream_progress.set_fraction(progress/float(3)) # 3 stages

    def stream(self, button, userdata=None):
        if StreamManager.get_stream_manager().is_streaming() is False:
            self.start_stream()
        else:
            self.stop_stream()

    def start_stream(self):
        StreamSettings.stream_username = self.username_entry.get_text()
        StreamSettings.stream_key = self.stream_key_entry.get_text()
        StreamSettings.save()

        StreamManager.get_stream_manager().start_streaming()
        self.stream_button.set_label("Stop")

    def stop_stream(self):
        StreamManager.get_stream_manager().stop_streaming()
        self.stream_button.set_label("Go Live!")

    def remember_me(self, checkbox, userdata=None):
        """ Called when the 'Remember Me' checkbox is pressed. """
        StreamSettings.remember_me = checkbox.get_active()
        StreamSettings.save()

    def quit(self, button, userdata=None):
        self.dialog.hide()
        return True # Prevents the window from being destroyed. We only want to hide.
