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
import os
import shutil
import tempfile
import lxml.etree
import openmediavault
import openmediavault.config.database
import openmediavault.config.object

class DatabaseTestCase(unittest.TestCase):
	def setUp(self):
		# Tell the database implementation to use the test database.
		openmediavault.setenv("OMV_CONFIG_FILE", "%s/data/config.xml" %
			os.getcwd())

	def _use_tmp_config_database(self):
		"""
		Create a copy of the database and use this. This is useful if the
		database is modified during the test.
		"""
		config_file = "%s/data/config.xml" % os.getcwd()
		(fh, tmp_config_file) = tempfile.mkstemp();
		shutil.copy(config_file, tmp_config_file)
		openmediavault.setenv("OMV_CONFIG_FILE", tmp_config_file)

	def test_constructor(self):
		db = openmediavault.config.Database()
		self.assertIsNotNone(db)

	def test_get_1(self):
		db = openmediavault.config.Database()
		obj = db.get("conf.system.time")
		self.assertIsInstance(obj, openmediavault.config.Object)
		self.assertEqual(obj.get("ntp.timeservers"), "pool.ntp.org")

	def test_get_2(self):
		db = openmediavault.config.Database()
		obj = db.get("conf.system.apt.distribution")
		self.assertIsInstance(obj, openmediavault.config.Object)
		self.assertFalse(obj.get("proposed"))

	def test_get_iterable(self):
		db = openmediavault.config.Database()
		objs = db.get("conf.system.notification.notification")
		self.assertIsInstance(objs, list)
		self.assertTrue(0 < len(objs))
		self.assertIsInstance(objs[0], openmediavault.config.Object)

	def test_get_by_filter_1(self):
		db = openmediavault.config.Database()
		objs = db.get_by_filter("conf.system.notification.notification",
			openmediavault.config.DatabaseFilter({
				'operator': 'stringEquals',
				'arg0': 'uuid',
				'arg1': '03dc067d-1310-45b5-899f-b471a0ae9233'
			}))
		self.assertIsInstance(objs, list)
		self.assertEqual(len(objs), 1)

	def test_get_by_filter_2(self):
		db = openmediavault.config.Database()
		objs = db.get_by_filter("conf.system.notification.notification",
			openmediavault.config.DatabaseFilter({
				'operator': 'stringContains',
				'arg0': 'id',
				'arg1': 'monit'
			}))
		self.assertIsInstance(objs, list)
		self.assertEqual(len(objs), 5)

	def test_exists(self):
		db = openmediavault.config.Database()
		exists = db.exists("conf.system.notification.notification",
			openmediavault.config.DatabaseFilter({
				'operator': 'stringEquals',
				'arg0': 'id',
				'arg1': 'smartmontools'
			}))
		self.assertTrue(exists)

	def test_get_list_elements(self):
		query = openmediavault.config.DatabaseGetQuery("conf.service.rsyncd")
		self.assertEqual(query._get_array_properties(), [ "module", "user" ])

	def test_get_query(self):
		query = openmediavault.config.DatabaseGetQuery("conf.system.time")
		self.assertEqual(query.xpath, "//system/time")

	def test_get_query_iterable(self):
		query = openmediavault.config.DatabaseGetQuery(
			"conf.system.notification.notification",
			"394cd565-e463-4094-a6ab-12e80270e9b4")
		self.assertEqual(query.xpath, "//system/notification/notifications/" \
			"notification[uuid='394cd565-e463-4094-a6ab-12e80270e9b4']")

	def test_filter_query_1(self):
		query = openmediavault.config.DatabaseGetByFilterQuery(
			"conf.system.notification.notification",
			openmediavault.config.DatabaseFilter({
				'operator': 'stringContains',
				'arg0': 'id',
				'arg1': 'monit'
			}))
		self.assertEqual(query.xpath, "//system/notification/notifications/" \
			"notification[contains(id,'monit')]")

	def test_filter_query_2(self):
		query = openmediavault.config.DatabaseGetByFilterQuery(
			"conf.system.network.proxy",
			openmediavault.config.DatabaseFilter({
				'operator': 'or',
				'arg0': {
					'operator': '=',
					'arg0': 'port',
					'arg1': 8080
				},
				'arg1': {
					'operator': 'equals',
					'arg0': 'port',
					'arg1': 4443
				}
			}))
		self.assertEqual(query.xpath, "//system/network/proxy[(port=8080 or " \
			"port=4443)]")

	def test_is_unique_by_filter(self):
		db = openmediavault.config.Database()
		obj = db.get("conf.system.notification.notification",
			"c1cd54af-660d-4311-8e21-2a19420355bb")
		self.assertIsInstance(obj, openmediavault.config.Object)
		self.assertTrue(db.is_unique(obj, "uuid"))

	def test_is_referenced_query_1(self):
		db = openmediavault.config.Database()
		obj = db.get("conf.system.sharedfolder",
			"339bd101-5744-4017-9392-01a156f15ab9")
		self.assertIsInstance(obj, openmediavault.config.Object)
		self.assertTrue(db.is_referenced(obj))

	def test_is_referenced_query_2(self):
		db = openmediavault.config.Database()
		obj = db.get("conf.system.sharedfolder",
			"91fe93fc-ef9d-11e6-9b06-000c2900c2de")
		self.assertIsInstance(obj, openmediavault.config.Object)
		self.assertFalse(db.is_referenced(obj))

	def test_delete(self):
		self._use_tmp_config_database()
		db = openmediavault.config.Database()
		obj = db.get("conf.system.notification.notification",
			"03dc067d-1310-45b5-899f-b471a0ae9233")
		self.assertIsInstance(obj, openmediavault.config.Object)
		query = openmediavault.config.DatabaseDeleteQuery(obj)
		self.assertEqual(query.xpath, "//system/notification/notifications/" \
			"notification[uuid='03dc067d-1310-45b5-899f-b471a0ae9233']")
		query.execute()
		self.assertIsInstance(query.response, openmediavault.config.Object)
		self.assertEqual(query.response.get("id"), "monitmemoryusage")

	def test_delete_by_filter(self):
		self._use_tmp_config_database()
		db = openmediavault.config.Database()
		objs = db.delete_by_filter("conf.system.notification.notification",
			openmediavault.config.DatabaseFilter({
				'operator': 'stringContains',
				'arg0': 'id',
				'arg1': 'monit'
			}))
		self.assertIsInstance(objs, list)
		self.assertEqual(len(objs), 5)

	def test_dict_to_elements(self):
		#  Create a fake query object to access the helper method.
		query = openmediavault.config.DatabaseGetQuery(
			"conf.system.notification.notification")
		root = lxml.etree.Element("config")
		query._dict_to_elements({
			'a': 1,
			'b1': False,
			'b2': True,
			'c': { 'x': "test" },
			'd': 5.45,
			'f': { 'z': [ 1, 2, 3 ] },
			'g': [ 'x', 'y' ]
		}, root)
		"""
		The result XML tree should look like:
		<config>
			<a>1</a>
			<b1>0</b1>
			<b2>1</b2>
			<c>
				<x>test</x>
			</c>
			<d>5.45</d>
			<f>
				<z>1</z>
				<z>2</z>
				<z>3</z>
			</f>
			<g>x</g>
			<g>y</g>
		</config>
		"""
		#xml = lxml.etree.tostring(root, encoding="unicode")
		#self.assertEqual(xml, "<config><b1>0</b1><c><x>test</x></c>" \
		#	"<b2>1</b2><f><z>1</z><z>2</z><z>3</z></f><d>5.45</d>" \
		#	"<a>1</a><g>x</g><g>y</g></config>")

	def test_set_1(self):
		self._use_tmp_config_database()
		db = openmediavault.config.Database()
		obj = db.get("conf.system.apt.distribution")
		self.assertIsInstance(obj, openmediavault.config.Object)
		self.assertFalse(obj.get("proposed"))
		obj.set("proposed", True)
		old_obj = db.set(obj)
		self.assertIsInstance(old_obj, openmediavault.config.Object)
		self.assertFalse(old_obj.get("proposed"))
		obj = db.get("conf.system.apt.distribution")
		self.assertIsInstance(obj, openmediavault.config.Object)
		self.assertTrue(obj.get("proposed"))

if __name__ == "__main__":
	unittest.main()
