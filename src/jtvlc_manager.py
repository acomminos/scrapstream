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

from process_manager import ProcessManager
from stream_settings import StreamSettings
import os

class JTVLCManager(ProcessManager)

    def __init__(self):
        super().__init__()

def get_command(self):
    jtvlc_path = os.path.join(os.getcwd(), "jtvlc-lin-0.41", "jtvlc")
    jtvlc_args = [jtvlc_path,
                  StreamSettings.stream_username,
                  StreamSettings.stream_key,
                  StreamSettings.sdp_path]
