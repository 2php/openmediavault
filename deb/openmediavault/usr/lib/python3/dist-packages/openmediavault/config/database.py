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
__all__ = [
	"Database",
	"DatabaseException",
	"DatabaseFilter",
	"DatabaseGetQuery",
	"DatabaseFilterQuery"
]

import openmediavault.collections
import openmediavault.config.datamodel
import openmediavault.config.object

class DatabaseException(Exception):
	pass

class DatabaseFilter(openmediavault.collections.DotDict):
	pass

class Database(object):
	def get(self, id, uuid=None):
		"""
		Get the specified configuration object.
		:param id:		The data model identifier, e.g. 'conf.service.ftp'.
		:param uuid:	The UUID of an configuration object. Defaults to None.
		:returns:		Depending on the configuration object and whether
						*uuid* is set, a list of configuration objects or
						a single object is returned.
		"""
		result = None
		# Get the specified data model.
		model = openmediavault.config.Datamodel(id)
		#// Create the query builder.
		#$queryBuilder = new DatabaseBackendQueryBuilder($id);
		#$xpath = $queryBuilder->buildGetQuery($uuid);
		#// Redirect the query to the database backend.
		#if ((TRUE === $model->isIterable()) && is_null($uuid))
		#	$data = $this->getBackend()->getList($xpath);
		#else
		#	$data = $this->getBackend()->get($xpath);
		#if (is_null($data)) {
		#	throw new DatabaseException("Failed to execute XPath query '%s'.",
		#	  $xpath);
		#}
		#if ((TRUE === $model->isIterable()) && is_null($uuid)) {
		#	result = [];
		#	foreach ($data as $datak => $datav) {
		#		$object = new ConfigObject($id);
		#		$object->setAssoc($datav, FALSE);
		#		result[] = $object;
		#	}
		#} else {
		#	result = new ConfigObject($id);
		#	result->setAssoc($data, FALSE);
		#}
		return result;

	def get_by_filter(self, filter, max_result=None):
		"""
		Get the iterable configuration objects that are matching the specified
		constraints.
		:param id:			The data model identifier, e.g. 'conf.service.ftp'.
		:param filter:		A filter specifying constraints on the objects
							to retrieve.
							``
							Example 1:
							{
								"operator": "stringEquals",
								"arg0": "fsname",
								"arg1": "xyz"
							}

							Example 2:
							{
								"operator": "and",
								"arg0": {
									"operator": "stringEquals",
									"arg0": "type",
									"arg1": "bond"
								},
								"arg1": {
									"operator": "stringEquals",
									"arg0": "devicename",
									"arg1": "bond0"
								}
							}
							``
		:param max_result:	The maximum number of objects that are returned.
							Defaults to None.
		:returns:			An array containing the requested configuration
							objects. If *max_result* is set to 1, then the
							first found object is returned.
							In this case the method does not return a list
							of configuration objects.
		"""
		assert(isinstance(filter, DatabaseFilter))
		# Get the specified data model.
		model = openmediavault.config.Datamodel(id)
		#// Is the configuration object iterable?
		#if (FALSE === $model->isIterable()) {
		#	throw new \InvalidArgumentException(sprintf(
		#	  "The configuration object '%s' is not iterable.",
		#	  $model->getId()));
		#}
		#// Build the query predicate.
		#$queryBuilder = new DatabaseBackendQueryBuilder($id);
		#$xpath = $queryBuilder->buildQueryByFilter(filter);
		#// Redirect the query to the database backend.
		#$data = $this->getBackend()->getList($xpath);
		#// Create the configuration objects.
		#result = [];
		#foreach ($data as $datak => $datav) {
		#	if (!is_null($maxResult) && ($datak >= $maxResult))
		#		continue;
		#	$object = new ConfigObject($id);
		#	$object->setAssoc($datav, FALSE);
		#	result[] = $object;
		#}
		#if (1 == $maxResult) {
		#	if (empty(result)) {
		#		throw new DatabaseException(sprintf(
		#		  "The XPath query '%s' does not return the requested ".
		#		  "number of %d object(s).", $xpath, $maxResult));
		#	}
		#	result = result[0];
		#}
		#return result;

	def exists(self, id, filter=None):
		"""
		Check if on or more configuration object of the specified data
		model exists.
		:param id:		The data model identifier.
		:param filter:	A filter specifying constraints on the objects
						to retrieve. Defaults to NULL.
						``
						Example:
						{
							"operator": "not",
							"arg0": {
								"operator": "stringEquals",
								"arg0": "type",
								"arg1": "vlan"
							}
						}
						``
		:returns:		True if at least one configuration object exists,
						otherwise False.
		"""
		if not filter is None:
			assert(isinstance(filter, DatabaseFilter))
		# Get the specified data model.
		model = openmediavault.config.Datamodel(id)
		# Create the query builder.
		#$queryBuilder = new DatabaseBackendQueryBuilder($id);
		#$xpath = $queryBuilder->buildExistsQuery(filter);
		#return $this->getBackend()->exists($xpath);

	def is_referenced(self, obj):
		"""
		Check if the specified object is referenced.
		:param obj:	The configuration object to use.
		:returns:	True if the object is referenced, otherwise False.
		"""
		assert(isinstance(obj, openmediavault.config.Object))
		#if (FALSE === $object->isReferenceable()) {
		#	throw new DatabaseException(
		#	  "The configuration object '%s' can not be referenced.",
		#	  $object->getModelId());
		#}
		#// Create the query builder.
		#$queryBuilder = new DatabaseBackendQueryBuilder($object->getModelId());
		#$xpath = $queryBuilder->buildIsReferencedQuery($object);
		#return $this->getBackend()->exists($xpath);

	def is_unique(self, obj, property):
		"""
		Check if a configuration object with the value of the specified
		property is unique.
		:param obj:			The configuration object to use.
		:param property:	The name of the data model property.
		:returns:			True if no configuration object with the same
							property value exists, otherwise False.
		"""
		return self.is_unique_by_filter(obj, DatabaseFilter({
				'operator': 'stringEquals',
				'arg0': property,
				'arg1': obj.get(property)
			}))

	def is_unique_by_filter(self, obj, filter):
		"""
		Check if a configuration object with the specified constraints
		is unique.
		:param obj:		The configuration object to use.
		:param filter:	A filter specifying constraints on the objects
						to retrieve.
						``
						Example:
						{
							"operator": "stringEquals",
							"arg0": "sharename",
							"arg1": "Movies"
						}
						``
		:returns:		True if no configuration object with the same
						property values (specified by the filter) exists,
						otherwise False.
		"""
		assert(isinstance(obj, openmediavault.config.Object))
		assert(isinstance(filter, DatabaseFilter))
		#// If the object is iterable and not new, then we need to modify the
		#// filter to do not find the object itself.
		#if ((FALSE === $object->isNew()) && (TRUE === $object->isIterable())) {
		#	$idProperty = $object->getModel()->getIdProperty();
		#	filter = [
		#		"operator" => "and",
 		#		"arg0" => [
 		#			"operator" => "stringNotEquals",
 		#			"arg0" => $idProperty,
 		#			"arg1" => $object->get($idProperty)
 		#		],
 		#		"arg1" => filter
		#	];
		#}
		#$objects = $this->getByFilter($object->getModelId(), filter);
		#return (0 == count($objects));

class DatabaseQuery(object):
	def __init__(self, id):
		"""
		:param id: The data model identifier, e.g. 'conf.service.ftp.share'.
		"""
		self._model = openmediavault.config.Datamodel(id)

	@property
	def model(self):
		"""
		Get the data model as JSON object.
		:returns: Returns the data model as JSON object.
		"""
		return _model

	def __str__(self):
		raise NotImplementedError()

class DatabaseFilterQuery(DatabaseQuery):
	def __init__(self, id, filter):
		assert(isinstance(filter, DatabaseFilter))
		if not filter:
			raise ValueError("Filter must not be empty.")
		super().__init__(id)
		self._filter = filter

	@property
	def filter(self):
		return self._filter

	def __str__(self):
		"""
		Build the predicate for the specified filter.
		Supported operators:
		.-------------------------------------------------.
		| operator         | arg0          | arg1         |
		|------------------|---------------|--------------|
		| and              | assoc. array  | assoc. array |
		| or               | assoc. array  | assoc. array |
		| equals           | property name | value        |
		| notEquals        | property name | value        |
		| enum             | property name | array        |
		| stringEquals     | property name | value        |
		| stringNotEquals  | property name | value        |
		| stringContains   | property name | value        |
		| stringStartsWith | property name | value        |
		| stringEnum       | property name | array        |
		| not              | assoc. array  |              |
		| less             | property name | value        |
		| greater          | property name | value        |
		| lessEqual        | property name | value        |
		| greaterEqual     | property name | value        |
		'-------------------------------------------------'
		Example 1:
		[type='bond' and devicename='bond0']
		The filter for the above predicate:
		[
			"operator": "and",
			"arg0": [
				"operator" => "stringEquals",
				"arg0" => "type",
				"arg1" => "bond"
			],
			"arg1": [
				"operator" => "stringEquals",
				"arg0" => "devicename",
				"arg1" => "bond0"
			]
		]
		Example 2:
		[type='bond' and contains(slaves,'eth0')]
		The filter for the above predicate:
		[
			"operator": "and",
			"arg0": [
				"operator" => "stringEquals",
				"arg0" => "type",
				"arg1" => "bond"
			],
			"arg1": [
				"operator" => "stringContains",
				"arg0" => "slaves",
				"arg1" => "eth0"
			]
		]
		Example 3:
		[not type='vlan']
		The filter for the above predicate:
		[
			"operator": "not",
			"arg0": [
				"operator" => "stringEquals",
				"arg0" => "type",
				"arg1" => "vlan"
			]
		]
		Example 4:
		[
			"operator" => "and",
			"arg0" => [
		   		"operator" => "stringNotEquals",
				"arg0" => "uuid",
				"arg1" => $object->get("uuid")
			],
			"arg1" => [
				"operator" => "and",
				"arg0" => [
		 		"operator" => "stringEquals",
		 		"arg0" => "mntentref",
		 		"arg1" => $object->get("mntentref")
				],
				"arg1" => [
		 		"operator" => "stringEquals",
		 		"arg0" => "reldirpath",
		 		"arg1" => $object->get("reldirpath")
				]
			]
		]
		"""
		if not "operator" in filter:
			raise KeyError("Invalid filter, the field 'operator' is missing.")
		result = ""
		if filter['operator'] in [ 'and', 'or' ]:
			result = sprintf("(%s %s %s)",
			  $this->buildPredicate(filter['arg0']),
			  filter['operator'],
			  $this->buildPredicate(filter['arg1']));
		elif filter['operator'] in [ '=', 'equals' ]:
			result = sprintf("%s=%s", filter['arg0'], filter['arg1']);
		elif filter['operator'] in [ '!=', 'notEquals' ]:
			result = sprintf("%s!=%s", filter['arg0'], filter['arg1']);
		elif "enum" == filter['operator']:
			$parts = [];
			foreach (filter['arg1'] as $enumk => $enumv) {
				$parts[] = sprintf("%s=%s", filter['arg0'], $enumv);
			}
			result = sprintf("(%s)", implode(" or ", $parts));
		elif filter['operator'] in [ '==', 'stringEquals' ]:
			result = sprintf("%s=%s", filter['arg0'],
			  escapeshellarg(filter['arg1']));
		elif filter['operator'] in [ '!==', '!=', 'stringNotEquals' ]:
			result = sprintf("%s!=%s", filter['arg0'],
			  escapeshellarg(filter['arg1']));
		elif "stringContains" == filter['operator']:
			result = sprintf("contains(%s,%s)", filter['arg0'],
			  escapeshellarg(filter['arg1']));
		elif "stringStartsWith" == filter['operator']:
			result = sprintf("starts-with(%s,%s)", filter['arg0'],
			  escapeshellarg(filter['arg1']));
		elif "stringEnum" == filter['operator']:
			$parts = [];
			foreach (filter['arg1'] as $enumk => $enumv) {
				$parts[] = sprintf("%s=%s", filter['arg0'],
				  escapeshellarg($enumv));
			}
			result = sprintf("(%s)", implode(" or ", $parts));
		elif filter['operator'] in [ '!', 'not' ]:
			result = sprintf("not(%s)",
			  $this->buildPredicate(filter['arg0']));
		elif filter['operator'] in [ '<', 'less' ]:
			result = sprintf("%s<%s", filter['arg0'], filter['arg1']);
		elif filter['operator'] in [ '>', 'greater' ]:
			result = sprintf("%s>%s", filter['arg0'], filter['arg1']);
		elif filter['operator'] in [ '<=', 'lessEqual' ]:
			result = sprintf("%s<=%s", filter['arg0'], filter['arg1']);
		elif filter['operator'] in [ '>=', 'greaterEqual' ]:
			result = sprintf("%s>=%s", filter['arg0'], filter['arg1']);
		else:
			raise ValueError("The operator '%s' is not defined." %
				filter['operator'])
		return result

class DatabaseGetQuery(DatabaseQuery):
	def __init__(self, id, identifier=None):
		super().__init__(id)
		self._identifier = identifier

	@property
	def identifier(self):
		return self._identifier

	def __str__(self):
		result = self.model.queryinfo['xpath']
		if self.model.is_iterable and not self.identifier is None:
			result = str(DatabaseFilterQuery(DatabaseFilter({
					'operator': 'stringEquals',
					'arg0': self.model.queryinfo['idproperty'],
					'arg1': self.identifier
				 }))
		return result
