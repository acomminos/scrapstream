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

class ScrapIndicator(object):

    def __init__(self):
        self.indicator = appindicator.Indicator.new("scrapstream-client", "account-logged-in", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # create a menu
        menu = Gtk.Menu()

        # create items
        stream_title = "Go Live!"
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

        quit_title = "Quit Scrapstream"
        quit_item = Gtk.MenuItem(quit_title)
        quit_item.connect("activate", Gtk.main_quit, quit_title)
        menu.append(quit_item)
        quit_item.show()

        self.indicator.set_menu(menu)

        # Create stream window
        self.stream_window = StreamWindow()

    def start_stream(self, widget, data):
        self.stream_window.show()

    def show_settings(self, widget, data):
        #settings_window = Setting
        print "Show settings"