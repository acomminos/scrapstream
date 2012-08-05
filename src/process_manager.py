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

import subprocess
import abc

class ProcessManager(object):
	""" ProcessManager is a manager for a process executed by the subprocess module.

	It exists so that we can have a common interface for checking the status of an executed process-
	no need to muck around with subprocess polling methods, ProcessManager wraps these for ease of use.

	The method get_command(self) must be implemented in subclasses.
	"""

	__metaclass__ = abc.ABCMeta

	def __init__(self):
		self.process_started = False
		self.process_instance = None

	def start(self):
		self.process_started = True
		self.process_instance = subprocess.Popen(get_command())

	def stop(self, wait=False):
		if self.process_instance is not None:
			self.process_instance.terminate()
			if wait: self.process_instance.wait()
			self.process_started = False

	def is_started(self):
		""" Returns whether or not the process has been started.
			Resets after process termination. """
		return self.process_started

	def is_running(self):
		""" Returns whether or not the process is currently running. """
    	if self.process_instance is None:
        	return False
   		else:
        	return self.process_instance.poll() is None

	@abc.abstractmethod
	def get_command(self):
		return
