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

from gi.repository import Gtk, Gdk
import json
import os

SECTION_NAME = 'DEFAULT'

DEFAULTS = {
    'username': '',
    'stream_key': '',
    'remember_me': False,
    'capture_x': 0,
    'capture_y': 0,
    'capture_width': Gdk.Screen.get_default().get_width(),
    'capture_height': Gdk.Screen.get_default().get_height(),
    'output_width': Gdk.Screen.get_default().get_width(),
    'output_height': Gdk.Screen.get_default().get_height(),
    'frame_rate': 30,
    'audio_source_id': 'Microphone',
    'audio_youtube_url': '',
    'audio_file': '',
    'overlays': []
}

CONFIG_DIR = os.getenv('XDG_CONFIG_HOME')
if CONFIG_DIR is None:
    CONFIG_DIR = os.path.expanduser('~/.config')

CONFIG_PATH = "%s/scrapstream.conf" % CONFIG_DIR

# Initial load of configuration file, occurs when module is first imported
try:
    with open(CONFIG_PATH, 'r') as file:
        config = json.load(file)
        # Set default if there exists no key for each property
        for key, value in DEFAULTS.items():
            if key not in config:
                config[key] = value
except FileNotFoundError:
    print("Creating default config file.")
    config = DEFAULTS
except IOError:
    config = DEFAULTS

def get_config():
    '''Returns a mutable dictionary of the current settings.'''
    return config

def save():
    '''Saves the current configuration to disk.'''
    config_file = open(CONFIG_PATH, 'w')
    json.dump(config, config_file, sort_keys=True, indent=4)
    print("Configuration saved.")
