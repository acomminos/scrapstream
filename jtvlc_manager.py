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

# Example JTVLC command:
# jtvlc acomminos live_32117398_9ziSWTnePUNdfFLowt30egliPvatUx ~/.scrapstream.sdp

import jtvlc

stream_username = ""
stream_key = ""

def run_jtvlc():
    """ Creates a JTVLC instance with the SDP file created by VLC. """
    jtvlc_path = os.path.join(os.getcwd(), JTVLC_FOLDER, "jtvlc")
    jtvlc_args = [jtvlc_path,
                  stream_username,
                  stream_key,
                  vlc_manager.sdp_path]
    subprocess.Popen(jtvlc_args)

def set_credentials(username, stream_key):
    stream_username = username
    stream_key = stream_key