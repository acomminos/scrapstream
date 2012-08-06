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
from stream_settings import StreamSettings
from jtvlc_manager import JTVLCManager
from vlc_manager import VLCManager

class StreamMonitor(threading.Thread):

    def __init__(self, manager):
        super(StreamMonitor, self).__init__()
        self.thread_running = True
        self.monitoring = False
        self.period = 2
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

    def check_running(self):
        print "VLC streaming: %r\nJTVLC running: %r\n-------------------" % (self.monitor.is_vlc_streaming(), self.monitor.is_jtvlc_running())


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
        self.vlc_manager = VLCManager()
        self.jtvlc_manager = JTVLCManager()
        self.callbacks = []

    def start_streaming(self):
        self.streaming = True

        self.stream_monitor.start_monitoring()

    def stream_update(self):        
        # Start VLC
        if self.is_vlc_running() is False:
            if self.vlc_manager.is_started() is False:
                # Start VLC if has not started and is not running
                self.vlc_manager.start()
            else:
                # Throw error if VLC has started and is not running
                #self.error()
                self.stop_streaming()
                pass

        # Start JTVLC
        if self.is_jtvlc_running() is False and self.is_vlc_streaming():
            if self.jtvlc_manager.is_started() is False:
                # Start JTVLC if has not started and is not running
                self.jtvlc_manager.start()
            else:
                # Throw error if JTVLC has started and is not running
                #self.error()
                self.stop_streaming()
                pass

        for callback in self.callbacks:
            callback(self)

    def stop_streaming(self):
        self.streaming = False

        self.stream_monitor.stop_monitoring()
        self.vlc_manager.stop()
        self.jtvlc_manager.stop()

        # Run the shutdown changes through the callbacks
        for callback in self.callbacks:
            callback(self)

    def shutdown(self):
        self.stop_streaming()
        self.stream_monitor.stop()

    def is_streaming(self):
        return self.streaming

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def unsubscribe(self, callback):
        self.callbacks.delete(callback)

    def is_vlc_running(self):
        return self.vlc_manager.is_running()

    def is_jtvlc_running(self):
        return self.jtvlc_manager.is_running()

    def is_vlc_streaming(self):
        """Returns whether or not VLC is streaming anything to scrapstream's SDP file."""
        try:
            f = open(StreamSettings.sdp_path, 'r')
            sdp_contents = f.read()
            if sdp_contents == '' or sdp_contents == '(null)':
                f.close()
                return False
            f.close()
            return True
        except IOError:
            return False
