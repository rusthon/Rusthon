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
		if instanceof(items, String):
			self[...].addAll( items.split("") )
		else:
			self[...].addAll( items )

	@property
	def length(self):
		return self[...].length
	@length.setter
	def length(self,n):
		self[...].length = n

	def __getitem__(self, index):
		if index < 0:
			index = self.length + index
		return self[...][index]

	def __setitem__(self, index, value):
		if index < 0:
			index = self.length + index
		self[...][index] = value

	def __getslice__(self, start, stop, step):
		if stop == null and step == null:
			return self[...].sublist( start )
		elif stop < 0:
			stop = self[...].length + stop
			return self[...].sublist(start, stop)

	def __add__(self, other):
		self[...].addAll( other[...] )
		return self

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

	def items(self):
		r = []
		for key in self.keys():
			value = self[ key ]
			r.append( [key,value] )
		return r

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

def isinstance(a, klass):
	## this will not work in dart, because 'is' test fails when klass is a variable
	#return JS("a is klass")
	return a.runtimeType.toString() == klass.toString()

def __getslice__(a, start, stop, step):
	if instanceof(a, String):
		if start != null and stop != null:
			b = a.substring( start, stop )
		elif start != null:
			b = a.substring( start )
		else:
			b = a
		if step != null:
			b = __reverse__(b)
		return b

def __reverse__(a):
	if instanceof(a, String):
		buff = new( StringBuffer() )
		n = a.length - 1
		while n >= 0:
			buff.write( a[n] )
			n -= 1
		return buff.toString()

def __test_if_true__( ob ):
	if instanceof(ob, String):
		return ob.length != 0
	elif instanceof(ob, Number):
		return ob != 0
	elif instanceof(ob, list):
		return ob.length != 0
	elif instanceof(ob, dict):
		return ob.length != 0
	elif ob != null:
		return True
