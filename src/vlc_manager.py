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

from process_manager import ProcessManager
from stream_settings import StreamSettings

class VLCManager(ProcessManager):

    def get_command(self):
        return  ["cvlc",
                "screen://",
                "input_stream",
                "--sout=#transcode{venc=x264{keyint=60,idrint=2},vcodec=h264,width=%(width)d,height=%(height)d,vb=300}:rtp{dst=127.0.0.1,port=1234,sdp=file://%(sdp_path)s}" 
                % {'width': StreamSettings.output_width, 'height': StreamSettings.output_height, 'sdp_path': StreamSettings.sdp_path},
                "--screen-fps", str(StreamSettings.frame_rate),
                "--screen-width", str(StreamSettings.capture_width),
                "--screen-height", str(StreamSettings.capture_height)]