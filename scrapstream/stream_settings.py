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

from configparser import SafeConfigParser, NoSectionError
from gi.repository import Gtk, Gdk
import os

class StreamSettings(object):

    SCRAPSTREAM_SECTION = "scrapstream-settings"
    SCRAPSTREAM_DIR = ".scrapstream"

    config_dir = "%s/%s" % (os.getenv("HOME"), SCRAPSTREAM_DIR)
    config_path = "%s/config" % config_dir

    # Capture settings
    capture_x = 0
    capture_y = 0
    capture_width = None
    capture_height = None
    output_width = None
    output_height = None
    frame_rate = 30

    # Credentials
    stream_key = ""
    remember_me = False

    @staticmethod
    def load():
        """ Loads the stream settings file. If not present, creates one. """

        # Plug in default GDK screen size values, in case not set
        screen = Gdk.Screen.get_default()
        StreamSettings.capture_width = StreamSettings.output_width = screen.get_width()
        StreamSettings.capture_height = StreamSettings.output_height = screen.get_height()
        
        try:
            if not os.path.exists(StreamSettings.config_dir):
                os.makedirs(StreamSettings.config_dir)

            open(StreamSettings.config_path) # Attempt opening the config file, will throw IOError if does not exist
            
            config = SafeConfigParser()
            config.read(StreamSettings.config_path)

            # Streaming
            if config.has_option(StreamSettings.SCRAPSTREAM_SECTION, "stream_key"):
                StreamSettings.stream_key = config.get(StreamSettings.SCRAPSTREAM_SECTION, "stream_key")
            if config.has_option(StreamSettings.SCRAPSTREAM_SECTION, "remember_me"):
                StreamSettings.remember_me = config.getboolean(StreamSettings.SCRAPSTREAM_SECTION, "remember_me")

            # Capture
            if config.has_option(StreamSettings.SCRAPSTREAM_SECTION, "capture_x"):
                StreamSettings.capture_x = config.getint(StreamSettings.SCRAPSTREAM_SECTION, "capture_x")
            if config.has_option(StreamSettings.SCRAPSTREAM_SECTION, "capture_y"):
                StreamSettings.capture_y = config.getint(StreamSettings.SCRAPSTREAM_SECTION, "capture_y")
            if config.has_option(StreamSettings.SCRAPSTREAM_SECTION, "capture_width"):
                StreamSettings.capture_width = config.getint(StreamSettings.SCRAPSTREAM_SECTION, "capture_width")
            if config.has_option(StreamSettings.SCRAPSTREAM_SECTION, "capture_height"):
                StreamSettings.capture_height = config.getint(StreamSettings.SCRAPSTREAM_SECTION, "capture_height")

            # Output
            if config.has_option(StreamSettings.SCRAPSTREAM_SECTION, "output_width"):
                StreamSettings.output_width = config.getint(StreamSettings.SCRAPSTREAM_SECTION, "output_width")
            if config.has_option(StreamSettings.SCRAPSTREAM_SECTION, "output_height"):
                StreamSettings.output_height = config.getint(StreamSettings.SCRAPSTREAM_SECTION, "output_height")
            if config.has_option(StreamSettings.SCRAPSTREAM_SECTION, "frame_rate"):
                StreamSettings.frame_rate = config.getint(StreamSettings.SCRAPSTREAM_SECTION, "frame_rate")

        except IOError:
            print("Config file does not exist! Will create on next save.")
        except NoSectionError:
            print("Config file is incorrectly configured! Will recreate on next save.")

    @staticmethod
    def save():
        config = SafeConfigParser()
        config.add_section(StreamSettings.SCRAPSTREAM_SECTION)
        config.set(StreamSettings.SCRAPSTREAM_SECTION, "stream_key", StreamSettings.stream_key if StreamSettings.remember_me else "")
        config.set(StreamSettings.SCRAPSTREAM_SECTION, "remember_me", "%r" % StreamSettings.remember_me)
        config.set(StreamSettings.SCRAPSTREAM_SECTION, "capture_x", "%d" % StreamSettings.capture_x)
        config.set(StreamSettings.SCRAPSTREAM_SECTION, "capture_y", "%d" % StreamSettings.capture_y)
        if StreamSettings.capture_width is not None:
            config.set(StreamSettings.SCRAPSTREAM_SECTION, "capture_width", "%d" % StreamSettings.capture_width)
        if StreamSettings.capture_height is not None:
            config.set(StreamSettings.SCRAPSTREAM_SECTION, "capture_height", "%d" % StreamSettings.capture_height)
        if StreamSettings.output_width is not None:
            config.set(StreamSettings.SCRAPSTREAM_SECTION, "output_width", "%d" % StreamSettings.output_width)
        if StreamSettings.output_height is not None:
            config.set(StreamSettings.SCRAPSTREAM_SECTION, "output_height", "%d" % StreamSettings.output_height)
        config.set(StreamSettings.SCRAPSTREAM_SECTION, "frame_rate", "%d" % StreamSettings.frame_rate)

        # Write configuration
        config_file = open(StreamSettings.config_path, 'w')
        config.write(config_file)
        print("Config file saved.")
