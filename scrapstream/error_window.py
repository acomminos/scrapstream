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

class ErrorWindow(object):

	def __init__(self, output=None):
		handlers = { "on_messagedialog1_close": self.quit }
		builder = Gtk.Builder()
		builder.add_from_file("xml/stream_error.glade")
		self.dialog = builder.get_object("messagedialog1")
		self.dialog.set_markup("FFMpeg has quit unexpectedly.")
		self.error_text = builder.get_object("text_buffer")
		builder.connect_signals(handlers)

		if output is not None:
			self.set_output(output)

	def show(self):
		self.dialog.show_all()

	def quit(self, widget, userdata=None):
		self.dialog.destroy()

	def set_output(self, output):
		self.error_text.set_text(output)
