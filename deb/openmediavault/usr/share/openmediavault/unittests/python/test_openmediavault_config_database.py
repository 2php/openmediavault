# -*- coding: utf-8 -*-
#
# This file is part of OpenMediaVault.
#
# @license   http://www.gnu.org/licenses/gpl.html GPL Version 3
# @author    Volker Theile <volker.theile@openmediavault.org>
# @copyright Copyright (c) 2009-2017 Volker Theile
#
# OpenMediaVault is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# OpenMediaVault is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenMediaVault. If not, see <http://www.gnu.org/licenses/>.
import unittest
import openmediavault.config.database
import openmediavault.config.object

class DatabaseTestCase(unittest.TestCase):
	def test_constructor(self):
		db = openmediavault.config.Database()

	def test_get(self):
		db = openmediavault.config.Database()
		db.get("conf.system.time")

	def test_get_iterable(self):
		db = openmediavault.config.Database()
		obj = db.get("conf.system.notification.notification",
			"c1cd54af-660d-4311-8e21-2a19420355bb")
		self.assertTrue(isinstance(obj, openmediavault.config.Object))
		self.assertEqual(obj.get("id"), "monitloadavg")

	def test_exists(self):
		db = openmediavault.config.Database()
		exists = db.exists("conf.system.notification.notification",
			openmediavault.config.DatabaseFilter({
				'operator': 'stringEquals',
				'arg0': 'id',
				'arg1': 'smartmontools'
			}))
		self.assertTrue(exists)

if __name__ == "__main__":
	unittest.main()
