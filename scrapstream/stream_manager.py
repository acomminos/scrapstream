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

from gi.repository import GLib
import threading
import time
from error_window import ErrorWindow
from ffmpeg_manager import FFMpegManager
from notification_manager import NotificationManager

class StreamThread(threading.Thread):

        def __init__(self, manager):
            super(StreamThread, self).__init__()
            self.manager = manager;

        def run(self):
            #NotificationManager.get_notification_manager().notify("Streaming started")
            return_code = self.manager.ffmpeg_manager.process.wait()
            if return_code == 1:
                print("FFMpeg has crashed.")
                self.error()

            GLib.idle_add(self.manager.send_callbacks)
            self.manager.thread = None

class StreamManager(threading.Thread):

    stream_manager = None

    def get_stream_manager():
        if StreamManager.stream_manager is None:
            StreamManager.stream_manager = StreamManager()
        return StreamManager.stream_manager

    def __init__(self):
        self.thread = None
        self.callbacks = []
        self.ffmpeg_manager = FFMpegManager()

    def error(self):
        """ Creates an error window informing the user that the passed process has crashed. """
        error_window = ErrorWindow()
        error_window.set_output(self.ffmpeg_manager.get_error())
        error_window.show()

    def start(self):
        assert self.thread == None
        self.ffmpeg_manager.start()
        self.thread = StreamThread(self)
        self.thread.start()

    def stop(self):
        self.ffmpeg_manager.stop()
        self.thread = None

    def is_running(self):
        if self.thread is not None:
            return self.thread.is_alive()
        return False

    def send_callbacks(self):
        for callback in self.callbacks:
            callback(self)

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def unsubscribe(self, callback):
        self.callbacks.delete(callback)
