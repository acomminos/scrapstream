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
import subprocess

#sys.path.append(os.path.join(os.getcwd(), "jtvlc"))
#from jtvlc import jtvlc
import vlc_manager

stream_username = ""
stream_key = ""

jtvlc_started = False
jtvlc_process = None

def run_jtvlc(username, key):
    global jtvlc_process, jtvlc_started
    """ Creates a JTVLC instance with the SDP file created by VLC. """
    jtvlc_path = os.path.join(os.getcwd(), "jtvlc-lin-0.41", "jtvlc")
    jtvlc_args = [jtvlc_path,
                  username,
                  key,
                  vlc_manager.sdp_path]
    jtvlc_process = subprocess.Popen(jtvlc_args, stderr=subprocess.STDOUT)#, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    jtvlc_started = True
    print "Created JTVLC with PID %d!" % jtvlc_process.pid

# DOESN'T WORK PLS FIX
def stop_jtvlc():
    """ Stops a JTVLC instance. """
    global jtvlc_process, jtvlc_started
    if jtvlc_process is not None and jtvlc_process.poll() is None:
        print "Killing JTVLC with PID %d..." % jtvlc_process.pid
        jtvlc_started = False
        jtvlc_process.terminate()
        jtvlc_process.wait()
        #jtvlc_process = None
    else:
        print "Can't kill JTVLC- it isn't running!"

def set_credentials(username, stream_key):
    stream_username = username
    stream_key = stream_key

def is_process_running():
    global jtvlc_process
    if jtvlc_process is None:
        return False
    else:
        return jtvlc_process.poll() is None

def get_output():
    global jtvlc_process
    return jtvlc_process.communicate()[0]