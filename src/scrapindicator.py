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
from gi.repository import AppIndicator3 as appindicator
from stream_window import StreamWindow
from aboutwindow import AboutWindow
import streammonitor
import vlc_manager
import jtvlc_manager

class ScrapstreamState(object):
    DISCONNECTED = 0
    FAILURE = 1
    VLC_RUNNING = 2
    JTVLC_RUNNING = 3
    STREAMING = 4

class ScrapIndicator(object):

    def __init__(self):
        self.indicator = appindicator.Indicator.new("scrapstream-client", "account-logged-in", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # create a menu
        menu = Gtk.Menu()

        stream_status_title = "Stream state"
        self.stream_status_item = Gtk.MenuItem(stream_status_title)
        self.stream_status_item.set_sensitive(False)
        menu.append(self.stream_status_item)
        self.stream_status_item.show()

        self.set_stream_state(ScrapstreamState.DISCONNECTED)

        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        separator.show()

        # create items
        stream_title = "Stream"
        stream_item = Gtk.MenuItem(stream_title)
        stream_item.connect("activate", self.start_stream, stream_title)
        menu.append(stream_item)
        stream_item.show()

        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        separator.show()

        settings_title = "Settings"
        settings_item = Gtk.MenuItem(settings_title)
        settings_item.connect("activate", self.show_settings, settings_title)
        menu.append(settings_item)
        settings_item.show()

        separator = Gtk.SeparatorMenuItem()
        menu.append(separator)
        separator.show()

        about_title = "About"
        about_item = Gtk.MenuItem(about_title)
        about_item.connect("activate", self.show_about, about_title)
        menu.append(about_item)
        about_item.show()

        quit_title = "Quit Scrapstream"
        quit_item = Gtk.MenuItem(quit_title)
        quit_item.connect("activate", self.quit, quit_title)
        menu.append(quit_item)
        quit_item.show()

        self.indicator.set_menu(menu)

        # Create stream window
        self.stream_window = StreamWindow()

        # Register update
        monitor = streammonitor.get_stream_monitor()
        monitor.subscribe(self.monitor_update)

    def start_stream(self, widget, data):
        self.stream_window.show()

    def show_settings(self, widget, data):
        #settings_window = Setting
        print "Show settings"

    def show_about(self, widget, data):
        about_window = AboutWindow()
        about_window.show()

    def monitor_update(self, monitor):
        if monitor.vlc_running and monitor.jtvlc_running:
            self.set_stream_state(ScrapstreamState.STREAMING)
        elif monitor.vlc_running:
            self.set_stream_state(ScrapstreamState.VLC_RUNNING)
        elif monitor.jtvlc_running:
            self.set_stream_state(ScrapstreamState.JTVLC_RUNNING)
        else:
            self.set_stream_state(ScrapstreamState.DISCONNECTED)

    def set_stream_state(self, state):
        stream_text = "State unknown!"
        indicator_icon = ""

        if state == ScrapstreamState.DISCONNECTED:
            stream_text = "Offline"
        elif state == ScrapstreamState.VLC_RUNNING:
            stream_text = "JTVLC not running"
        elif state == ScrapstreamState.JTVLC_RUNNING:
            stream_text = "VLC not running"
        elif state == ScrapstreamState.FAILURE:
            stream_text = "Broadcast Failed - See Status"
        elif state == ScrapstreamState.STREAMING:
            stream_text = "Online"

        self.stream_status_item.set_label(stream_text)

    def quit(self, widget, state):
        Gtk.main_quit()
        monitor = streammonitor.get_stream_monitor()
        monitor.stop()
        vlc_manager.stop_vlc()
        jtvlc_manager.stop_jtvlc()