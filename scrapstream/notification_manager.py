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

from gi.repository import Notify

class NotificationManager(object):

	singleton = None

	@staticmethod
	def get_notification_manager():
		if NotificationManager.singleton is None:
			NotificationManager.singleton = NotificationManager()
		return NotificationManager.singleton

	def __init__(self):
		Notify.init("Scrapstream")

	def notify(self, message, title="Scrapstream"):
		"""Creates and shows a notification with the specified message and title (if passed).
		Returns the created notification. """
		notification = Notify.Notification.new(title, message, "dialog-information")
		notification.show()
		return notification
