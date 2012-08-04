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
import vlc_manager
import jtvlc_manager

stream_monitor = None

def get_stream_monitor():
    global stream_monitor
    if stream_monitor is None:
        stream_monitor = StreamMonitor()
    return stream_monitor

class StreamMonitor(threading.Thread):

    def __init__(self):
        super(StreamMonitor, self).__init__()
        self.thread_running = True
        self.vlc_running = False
        self.jtvlc_running = False
        self.period = 2
        self.callbacks = []

    def stop(self):
        self.thread_running = False

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def unsubscribe(self, callback):
        self.callbacks.delete(callback)

    def run(self):
        while self.thread_running:
            self.check_running()

            for callback in self.callbacks:
                GLib.idle_add(callback) # Execute callback on main thread

            time.sleep(self.period)

    def check_running(self):
        self.vlc_running = self.is_vlc_streaming()
        self.jtvlc_running = self.is_jtvlc_streaming()
        print "VLC streaming: %r\nJTVLC running: %r\n-------------------" % (self.vlc_running, self.jtvlc_running)

    def is_vlc_streaming(self):
        """Returns whether or not VLC is streaming anything to scrapstream's SDP file."""
        try:
            f = open(vlc_manager.sdp_path, 'r')
            sdp_contents = f.read()
            if sdp_contents == '' or sdp_contents == '(null)':
                f.close()
                return False
            f.close()
            return True
        except IOError:
            return False

    def is_jtvlc_streaming(self):
        return jtvlc_manager.is_process_running()
