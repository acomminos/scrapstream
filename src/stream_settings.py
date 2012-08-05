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

import json
import os
import getpass

class StreamSettings(object):
	# Capture settings
	capture_width = 1440
	capture_height = 900
	output_width = 1440
	output_height = 900
	frame_rate = 30

	# Credentials
	stream_username = ""
	stream_key = ""

	# SDP
	sdp_name = ".scrapstream.sdp"
	sdp_path = "/home/%(username)s/%(sdp_name)s" % {'username': getpass.getuser(), 'sdp_name': sdp_name}
