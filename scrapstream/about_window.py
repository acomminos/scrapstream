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

class AboutWindow(object):

	def __init__(self):
		handlers = {"close": self.close}
		builder = Gtk.Builder()
		builder.add_from_file("xml/stream_about.glade")
		self.dialog = builder.get_object("aboutdialog1")
		builder.connect_signals(handlers)

	def show(self):
		self.dialog.show_all()

	def close(self, widget, userdata=None):
		self.dialog.destroy()