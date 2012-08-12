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

from ConfigParser import RawConfigParser
import os

class StreamSettings(object):

	config_path = "%s/.scrapstream-config" % os.getenv("HOME")
	config = None

	# Capture settings
	capture_width = 1920
	capture_height = 1080
	output_width = 1920
	output_height = 1080
	frame_rate = 30

	# Credentials
	stream_username = ""
	stream_key = ""
	remember_me = False

	# SDP
	sdp_name = ".scrapstream.sdp"
	sdp_path = "%(home)s/%(sdp_name)s" % {'home': os.getenv("HOME"), 'sdp_name': sdp_name}

	@staticmethod
	def load():
		""" Loads the stream settings file. If not present, creates one. """
#		config = RawConfigParser()
#		config.read(StreamSettings.config_path)

#		StreamSettings.stream_username = config.get("section", "stream_username")
#		StreamSettings.stream_key = config.get("section", "stream_key")
		pass
	@staticmethod
	def save():
#		with open(StreamSettings.config_path, 'w') as configfile:
#			config.write(configfile)
		pass
