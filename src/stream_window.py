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
import vlc_manager
import jtvlc_manager
from threading import Timer

class StreamWindow(object):

	def __init__(self):
		handlers = {
			"onLiveActivate": self.stream,
			"onCancelActivate": self.quit,
			"delete-event": self.quit
		}

		builder = Gtk.Builder()
		builder.add_from_file("xml/stream_dialog.glade")
		self.dialog = builder.get_object("dialog1")
		self.username_entry = builder.get_object("username_entry")
		self.stream_key_entry = builder.get_object("stream_key_entry")
		builder.connect_signals(handlers)

	def show(self):
		self.dialog.show_all()

	def stream(self, button, userdata=None):
		print "Starting streaming..."
		vlc_manager.start_vlc()

		username = self.username_entry.get_text()
		stream_key = self.stream_key_entry.get_text()
		jtvlc_manager.set_credentials(username, stream_key)

	def quit(self, button, userdata=None):
		vlc_manager.stop_vlc()
		self.dialog.hide()
		return True # Prevents the window from being destroyed. We only want to hide.