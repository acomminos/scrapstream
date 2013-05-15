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
from stream_settings import StreamSettings
from ffmpeg_manager import FFMpegManager
from notification_manager import NotificationManager

class StreamMonitor(threading.Thread):

    def __init__(self, manager):
        super(StreamMonitor, self).__init__()
        self.thread_running = True
        self.monitoring = False
        self.period = 0.25
        self.manager = manager

        # Start monitoring
        self.start()


    def start_monitoring(self):
        # Start required processes
        self.monitoring = True

    def stop_monitoring(self):
        self.monitoring = False

    def stop(self):
        self.thread_running = False
        self.join()

    def run(self):
        while self.thread_running:
            if self.monitoring:
                GLib.idle_add(self.manager.stream_update) # Execute callback on main thread

            time.sleep(self.period)

class StreamManager(object):

    stream_manager = None

    @staticmethod
    def get_stream_manager():
        if StreamManager.stream_manager is None:
            StreamManager.stream_manager = StreamManager()
        return StreamManager.stream_manager

    def __init__(self):
        self.streaming = False
        self.stream_monitor = StreamMonitor(self)
        self.callbacks = []
        self.ffmpeg_manager = FFMpegManager()

    def start_streaming(self):
        self.streaming = True
        self.ffmpeg_manager.start()
        #NotificationManager.get_notification_manager().notify("Streaming started")

        self.stream_monitor.start_monitoring()

    def stream_update(self):
        if self.ffmpeg_manager.is_error():
            print "FFMpeg has crashed."
            #self.stop_streaming()
            self.error()
            self.stop_streaming()
            return

        #for callback in self.callbacks:
        #    callback(self)

    def error(self):
        """ Creates an error window informing the user that the passed process has crashed. """
        error_window = ErrorWindow()
        error_window.set_output(self.ffmpeg_manager.get_error())
        error_window.show()

    def stop_streaming(self):
        self.streaming = False

        self.stream_monitor.stop_monitoring()
        self.ffmpeg_manager.stop()

        # Run the shutdown changes through the callbacks
        for callback in self.callbacks:
            callback(self)

        #NotificationManager.get_notification_manager().notify("Streaming stopped")

    def shutdown(self):
        self.stop_streaming()
        self.stream_monitor.stop()

    def is_streaming(self):
        return self.streaming

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def unsubscribe(self, callback):
        self.callbacks.delete(callback)
