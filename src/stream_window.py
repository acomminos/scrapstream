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
import streammonitor
from errorwindow import ErrorWindow

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
		self.stream_button = builder.get_object("stream_button")

		# Icons
		self.vlc_image = builder.get_object("vlc_image")
		self.jtvlc_image = builder.get_object("jtvlc_image")
		self.stream_image = builder.get_object("stream_image")

		# Status
		self.vlc_status = builder.get_object("vlc_status")
		self.jtvlc_status = builder.get_object("jtvlc_status")
		self.stream_status = builder.get_object("stream_status")

		# Progress
		self.stream_progress = builder.get_object("stream_progress")

		builder.connect_signals(handlers)

		# Monitor for vlc and jtvlc process changes
		monitor = streammonitor.get_stream_monitor()
		monitor.subscribe(self.monitor_update)

		self.streaming = False # Whether the user is making an attempt to stream

	def show(self):
		self.dialog.show_all()

	def monitor_update(self):
		monitor = streammonitor.get_stream_monitor()
		progress = float(0)
		vlc_image = ""
		vlc_status = ""

		if monitor.vlc_running:
			vlc_image = "xml/res/vlc-active.png"
			vlc_status = "Online"
			progress += 1
		else:
			vlc_image = "xml/res/vlc-inactive.png"
			vlc_status = "Offline"
		
		self.vlc_status.set_label(vlc_status)
		self.vlc_image.set_from_file(vlc_image)

		jtvlc_image = ""
		jtvlc_status = ""

		if monitor.jtvlc_running:
			jtvlc_image = "xml/res/jtv-active.png"
			jtvlc_status = "Online"
			progress += 1
		else:
			jtvlc_image = "xml/res/jtv-inactive.png"
			jtvlc_status = "Offline"
		
		self.jtvlc_status.set_label(jtvlc_status)
		self.jtvlc_image.set_from_file(jtvlc_image)

		stream_image = ""
		stream_status = ""
		if monitor.vlc_running and monitor.jtvlc_running:
			stream_image = "xml/res/stream-active.png"
			stream_status = "Online"
			progress += 1
		else:
			stream_image = "xml/res/stream-inactive.png"
			stream_status = "Offline"

		self.stream_status.set_label(stream_status)
		self.stream_image.set_from_file(stream_image)

		self.stream_progress.set_fraction(progress/float(3)) # 3 stages

		# Error monitoring
		if vlc_manager.is_process_running() is False and vlc_manager.vlc_started:
			# If VLC has started and is not running, error out
			print "VLC started but is not running! Error!"
			self.stop_stream()
			error_text = vlc_manager.get_output()
			ErrorWindow("VLC", error_text).show()

		if monitor.vlc_running and monitor.jtvlc_running is False:
			if jtvlc_manager.jtvlc_started is False:
				# Start JTVLC if VLC is running and it hasn't been started
				print "Starting JTVLC, VLC initialized..."
				username = self.username_entry.get_text()
				stream_key = self.stream_key_entry.get_text()
				jtvlc_manager.run_jtvlc(username, stream_key)
			else:
				# JTVLC is not running but has been started- halt.
				print "JTVLC started but is not running! Error!"
				self.stop_stream()
				error_text = vlc_manager.get_output()
				ErrorWindow("JTVLC", error_text).show()

	def stream(self, button, userdata=None):
		if self.streaming is False:
			self.start_stream()
		else:
			self.stop_stream()

	def start_stream(self):
		self.streaming = True
		vlc_manager.start_vlc()
		username = self.username_entry.get_text()
		stream_key = self.stream_key_entry.get_text()
		#jtvlc_manager.set_credentials(username, stream_key)
		self.stream_button.set_label(u"Stop")

	def stop_stream(self):
		self.streaming = False
		vlc_manager.stop_vlc()
		jtvlc_manager.stop_jtvlc()
		self.stream_button.set_label(u"Go Live!")

	def quit(self, button, userdata=None):
		self.dialog.hide()
		return True # Prevents the window from being destroyed. We only want to hide.