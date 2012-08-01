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

import sys
import os
import threading

sys.path.append(os.path.join(os.getcwd(), "jtvlc"))
from jtvlc import jtvlc
import vlc_manager

class JtvlcState(object):
    DISCONNECTED = 0
    CONNECTED = 1
    FAILED = 2

state = JtvlcState.DISCONNECTED

stream_username = ""
stream_key = ""

def run_jtvlc():
    """ Creates a JTVLC instance with the SDP file created by VLC. """

    if jtvlc.connect(stream_username, stream_key, vlc_manager.sdp_path):
        print "JTVLC established!"
        state = JtvlcState.CONNECTED
    else:
        print "JTVLC failed!"
        state = JtvlcState.FAILED

    """
    state = JtvlcState.DISCONNECTED
    jtvlc_path = os.path.join(os.getcwd(), JTVLC_FOLDER, "jtvlc")
    jtvlc_args = [jtvlc_path,
                  stream_username,
                  stream_key,
                  vlc_manager.sdp_path]
    subprocess.Popen(jtvlc_args)
    """
def set_credentials(username, stream_key):
    stream_username = username
    stream_key = stream_key