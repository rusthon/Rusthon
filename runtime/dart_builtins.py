# PythonJS builtins for Dart
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

dart_import('dart:collection')
dart_import('dart:math', 'Math')

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

	def __getslice__(self, start, stop, step):
		if stop == null and step == null:
			return self[...].sublist( start )
		elif stop < 0:
			stop = self[...].length + stop
			return self[...].sublist(start, stop)

	def append(self, item):
		self[...].add( item )

	def index(self, obj):
		return self[...].indexOf(obj)


tuple = list

#@dart.extends
class dict: #( HashMap ):
	'''
	HashMap can not be extended anymore:
		https://groups.google.com/a/dartlang.org/forum/#!msg/announce/Sj3guf3es24/YsPCdT_vb2gJ
	'''
	def __init__(self, map):
		#self[...] = new( Map() )
		#self[...].addAll( items )
		self[...] = map

	@property
	def length(self):
		return self[...].length

	def __getitem__(self, key):
		return self[...][key]

	def __setitem__(self, key, value):
		self[...][key] = value

	def contains(self, key):
		return self[...].containsKey(key)

	def keys(self):
		return self[...].keys.toList()

	def values(self):
		return self[...].values


def range(n):
	r = []
	i = 0
	while i < n:
		r.add( i )
		i += 1
	return r

def len(a):
	return a.length

def str(a):
	## TODO conversions to string
	return a