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

# Example VLC command:
# vlc screen:// -vvv input_stream --sout='#duplicate{dst=display, dst="transcode{venc=x264{keyint=60,idrint=2},scale=0.5,vcodec=h264,vb=300,acodec=mp4a,ab=32,channels=2,samplerate=44100}:rtp{dst=127.0.0.1,port=1234,sdp=file:///home/andrew/vlc.sdp}"}' --screen-width 1920 --screen-height 1080 --screen-fps 25

import subprocess

# Constants
sdp_path = "~/.scrapstream.sdp"

# Default streaming properties
capture_width = 1920
capture_height = 1080
capture_scale = 1
frame_rate = 30
vlc_pid = 0

def run_stream():
    """ Creates a new VLC instance with the properties. """
    vlc_command = "vlc screen:// -vvv input_stream \
    --sout='#duplicate{dst=display, dst=\"transcode{venc=x264{keyint=60,idrint=2},scale=%(scale)f,vcodec=h264,vb=300,acodec=mp4a,ab=32,channels=2,samplerate=44100}\
    :rtp{dst=127.0.0.1,port=1234,sdp=file:///home/andrew/vlc.sdp}\"}' \
    --screen-fps %(frame_rate)d --screen-width %(screen_width)d --screen-height %(screen_height)d" % \
    {'scale': capture_scale, 'screen_width': capture_width, 'screen_height': capture_height, 'frame_rate': frame_rate}
    
    subprocess.call(vlc_command, shell=True)