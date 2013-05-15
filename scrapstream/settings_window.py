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

from gi.repository import Gtk
from stream_settings import StreamSettings

class SettingsWindow(object):

    def __init__(self):
        handlers = { "save": self.save,
                     "discard": self.discard }
        builder = Gtk.Builder()
        builder.add_from_file("xml/stream_settings_dialog.glade")
        self.dialog = builder.get_object("dialog1")
        self.framerate_scale = builder.get_object("framerate_scale")
        self.fps_adjustment = builder.get_object("fps_adjustment")
        self.output_width = builder.get_object("output_width")
        self.output_height = builder.get_object("output_height")
        self.capture_x = builder.get_object("capture_x")
        self.capture_y = builder.get_object("capture_y")
        self.capture_width = builder.get_object("capture_width")
        self.capture_height = builder.get_object("capture_height")
        builder.connect_signals(handlers)

        self.load_settings()

    def load_settings(self):
        """Loads Scrapstream settings into the Settings window."""
        self.fps_adjustment.set_value(StreamSettings.frame_rate)
        self.output_width.set_text("%d" % StreamSettings.output_width)
        self.output_height.set_text("%d" % StreamSettings.output_height)
        self.capture_x.set_text("%d" % StreamSettings.capture_x)
        self.capture_y.set_text("%d" % StreamSettings.capture_y)
        self.capture_width.set_text("%d" % StreamSettings.capture_width)
        self.capture_height.set_text("%d" % StreamSettings.capture_height)

    def save_settings(self):
        """Saves settings changed in this window to the StreamSettings module, followed by a commit to the config file."""
        StreamSettings.frame_rate = self.fps_adjustment.get_value()
        StreamSettings.output_width = int(self.output_width.get_text())
        StreamSettings.output_height = int(self.output_height.get_text())
        StreamSettings.capture_x = int(self.capture_x.get_text())
        StreamSettings.capture_y = int(self.capture_y.get_text())
        StreamSettings.capture_width = int(self.capture_width.get_text())
        StreamSettings.capture_height = int(self.capture_height.get_text())
        StreamSettings.save()

    def show(self):
        self.dialog.show_all()

    def save(self, widget, userdata=None):
        try:
            self.save_settings()
        except:
            print "Could not save settings!"
        self.dialog.destroy()

    def discard(self, widget, userdata=None):
        self.dialog.destroy()
