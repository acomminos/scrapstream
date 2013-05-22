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

import signal
from gi.repository import Gtk, GObject
#from scrap_indicator import ScrapIndicator
from stream_settings import StreamSettings
from stream_window import StreamWindow
from notification_manager import NotificationManager

def main():
        StreamSettings.load() # Load settings

        GObject.threads_init() # Necessary to use multithreading
        #ScrapIndicator() TODO re-add ubuntu indicator, coding from arch with i3 now
        window = StreamWindow()
        window.show()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()

if __name__ == "__main__":
        main()
