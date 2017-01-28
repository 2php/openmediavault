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
__all__ = [ "ICommand" ]

import abc
import os
import shutil
import tempfile
import openmediavault

class ICommand(metaclass=abc.ABCMeta):
	@abc.abstractproperty
	def description(self):
		"""
		Get the module description.
		"""

	@abc.abstractmethod
	def validate_args(self, *args):
		"""
		Validate the command arguments.
		:param args: The command arguments to validate.
		:returns: Returns True if the arguments are valid, otherwise False.
		"""

	@abc.abstractmethod
	def usage(self, *args):
		"""
		Display the command help.
		:param args: The command arguments.
		"""

	@abc.abstractmethod
	def execute(self, *args):
		"""
		Execute the command.
		:param args: The command arguments.
		:returns: Returns the return code.
		"""

class CommandHelper():
	_backup_path = ""

	def mkBackup(self):
		"""
		Create a backup of the configuration database.
		:returns: Returns the path of the backup file.
		"""
		(fh, self._backup_path) = tempfile.mkstemp();
		shutil.copy(openmediavault.getenv("OMV_CONFIG_FILE"),
			self._backup_path)
		return self._backup_path

	def unlinkBackup(self):
		"""
		Unlink the backup of the configuration database.
		"""
		if not self._backup_path:
			raise RuntimeError("No configuration backup exists")
		os.unlink(self._backup_path)
		self._backup_path = ""

	def rollbackChanges():
		"""
		Rollback all changes in the configuration database.
		"""
		if not self._backup_path:
			raise RuntimeError("No configuration backup exists")
		shutil.copy(self._backup_path, openmediavault.getenv(
			"OMV_CONFIG_FILE"))
