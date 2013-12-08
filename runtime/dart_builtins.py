# PythonJS builtins for Dart
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

dart_import('dart:collection')

@dart.extends
class list( ListBase ):
	'''
	a List in Dart is growable if no size is given in the constructor,
	otherwise if size is given it becomes a fixed length list.

	Notes:
		https://code.google.com/p/dart/issues/detail?id=11201
		http://stackoverflow.com/questions/16247045/how-do-i-extend-a-list-in-dart
	'''
	def __init__(self, items):
		self[...] = new( List() )
		self[...].addAll( items )

	@property
	def length(self):
		return self[...].length
	@length.setter
	def length(self,n):
		self[...].length = n

	def __getitem__(self, index):
		return self[...][index]

	def __setitem__(self, index, value):
		self[...][index] = value

	def append(self, item):
		self[...].add( item )

	def index(self, obj):
		return self[...].indexOf(obj)


def range(n):
	r = []
	i = 0
	while i < n:
		r.add( i )
		i += 1
	return r

