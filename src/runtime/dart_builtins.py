# PythonJS builtins for Dart
# by Brett Hartshorn - copyright 2013
# License: "New BSD"

dart_import('dart:collection')
dart_import('dart:typed_data')
dart_import('dart:math', 'Math')

__random_gen__ = new(Math.Random())
def __random__(): return __random_gen__.nextDouble()


class float32vec:
	def __init__(self, items):
		self[...] = new( List() )
		self.length = items.length

		i = 0; s = 0
		while i < items.length:
			x = items[i]
			y = items[i+1]
			z = items[i+2]
			w = items[i+3]
			vec = new( Float32x4(x,y,z,w) )
			self[...].add( vec )
			i += 4


	def __getitem__(self, index):
		if index < 0: index = self.length + index

		let vec : float32x4 = self[...][ index // 4 ]
		lane = index % 4
		if lane == 0: return vec.x
		elif lane == 1: return vec.y
		elif lane == 2: return vec.z
		elif lane == 3: return vec.w

	def __setitem__(self, index, value):
		if index < 0: index = self.length + index

		vec = self[...][ index // 4 ]
		lane = index % 4
		if lane == 0: vec = vec.withX(value)
		elif lane == 1: vec = vec.withY(value)
		elif lane == 2: vec = vec.withZ(value)
		elif lane == 3: vec = vec.withW(value)

		self[...][ index // 4 ] = vec

	def __add__(self, other):
		arr = new( List() )
		for i, vec1 in enumerate( self[...] ):
			vec2 = other[...][ i ]
			arr.add( vec1+vec2 )

		v = inline("new float32vec([])")
		v.length = self.length
		v[...] = arr
		return v

	def __mul__(self, other):
		arr = new( List() )
		for i, vec1 in enumerate( self[...] ):
			vec2 = other[...][ i ]
			arr.add( vec1*vec2 )

		v = inline("new float32vec([])")
		v.length = self.length
		v[...] = arr
		return v


#@dart.extends
#class list( ListBase ):
class list:
	'''
	a List in Dart is growable if no size is given in the constructor,
	otherwise if size is given it becomes a fixed length list.

	Notes:
		https://code.google.com/p/dart/issues/detail?id=11201
		http://stackoverflow.com/questions/16247045/how-do-i-extend-a-list-in-dart
	'''

	## dart 1.3 ##
	#with inline: """
	#Iterator<dynamic> get iterator => new ListIterator<dynamic>(this);
	#Iterable map(f(dynamic element)) => new MappedListIterable(this, f);
	#"""


	def __init__(self, items):
		self[...] = new( List() )
		if instanceof(items, String):
			self[...].addAll( items.split("") )
		elif instanceof(items, list):
			self[...].addAll( items[...] )
		elif items is not None:
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

		if start == null and stop == null and step == null:
			return list( self[...] )
		else:
			if step == null: step = 1
			reverse = False
			if step < 0:
				step = step.abs()
				reverse = True

			a = new( List() )
			i = 0
			while i < self[...].length:
				a.add( self[...][i] )
				i += step

			if start == null: start = 0
			if stop == null: stop = a.length
			if start < 0:
				start = a.length + start
			if stop < 0:
				stop = a.length + stop

			if reverse:
				b = new( List() )
				b.addAll( a.reversed )
				return list( b.sublist(a.length-(start+1), stop) )
			else:
				return list( a.sublist(start, stop) )


	def __setslice__(self, start, stop, step, items):
		if start == null: start = 0
		if stop == null: stop = self[...].length
		stop -= start
		while stop != 0:
			self[...].removeAt(start)
			stop -= 1
		if instanceof(items, String):
			items = items.split('')
		elif instanceof(items, list):
			items = items[...]
		self[...].insertAll(start, items)


	def __add__(self, other):
		self[...].addAll( other[...] )
		return self

	def append(self, item):
		self[...].add( item )

	def index(self, obj):
		return self[...].indexOf(obj)

	def pop(self, n):
		return self[...].removeAt( n )

	def insert(self, i, o):
		if i < 0: i = self.length+i
		self[...].insert(i,o)


def tuple(a):
	return list(a)

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

def sum( arr ):
	a = 0
	for b in arr:
		a += b
	return a

def range(n):
	r = []
	i = 0
	while i < n:
		r.append( i )
		i += 1
	return r

def __range2(start, stop):
	r = []
	i = start
	while i < stop:
		r.append( i )
		i += 1
	return r

def len(a):
	return a.length

def str(a):
	if instanceof(a, String):
		return a
	elif instanceof(a, double):
		return a.toStringAsFixed(6)  ## TODO how to find best size for each double?
	else:
		return a.toString()

def isinstance(a, klass):
	## this will not work in dart, because 'is' test fails when klass is a variable
	#return JS("a is klass")
	return a.runtimeType.toString() == klass.toString()

def __getslice__(a, start, stop, step):
	if instanceof(a, String):
		if step != null:
			b = __reverse__(a)
		elif start != null and stop != null:
			if start < 0: start = a.length + start
			if stop < 0: stop = a.length + stop
			b = a.substring( start, stop )
		elif start != null and stop == null:
			if start < 0: start = a.length + start
			b = a.substring( start )
		elif stop != null:
			if stop < 0: stop = a.length + stop
			b = a.substring( 0, stop )
		else:
			b = a.substring(0)

		return b
	else:
		#return list.____getslice__(a, start, stop, step)
		return a.__getslice__(start, stop, step)

def __reverse__(a):
	if instanceof(a, String):
		buff = new( StringBuffer() )
		n = a.length - 1
		while n >= 0:
			buff.write( a[n] )
			n -= 1
		return buff.toString()

def __create_list( size ):
	a = list()
	for i in range(size):
		a.append( None )
	return a



with lowlevel:
	def __test_if_true__( ob ):
		if ob == True: return True
		elif ob == False: return False
		elif instanceof(ob, String):
			return ob.length != 0
		elif instanceof(ob, Number):
			return ob != 0
		elif instanceof(ob, list):
			return ob.length != 0
		elif instanceof(ob, dict):
			return ob.length != 0
		elif ob != null:
			return True

	def __sprintf(fmt, args):
		if instanceof(args, list):
			i = 0
			arr = []
			for part in fmt.split('%s'):
				arr.append(part)
				if i >= args.length:
					break
				else:
					arr.append( str(args[i]) )

				i += 1
			return arr[...].join('')

		else:
			return fmt.replaceFirst('%s', str(args))

	def __replace_method(o,a,b):
		if instanceof(a, String):
			return o.replaceAll(a,b)
		else:
			return o.replace(a,b)

	def __split_method(s):
		if instanceof(s, String):
			return s.split(' ')
		else:
			return s.split()

	def __upper_method(s):
		if instanceof(s, String):
			return s.toUpperCase()
		else:
			return s.upper()

	def __lower_method(s):
		if instanceof(s, String):
			return s.toLowerCase()
		else:
			return s.lower()

	def __lt__(a,b):
		if instanceof(a, String):
			return JS("a.codeUnitAt(0) < b.codeUnitAt(0)")
		else:
			return JS("a < b")

	def __gt__(a,b):
		if instanceof(a, String):
			return JS("a.codeUnitAt(0) > b.codeUnitAt(0)")
		else:
			return JS("a > b")


	def __lte__(a,b):
		if instanceof(a, String):
			return JS("a.codeUnitAt(0) <= b.codeUnitAt(0)")
		else:
			return JS("a <= b")

	def __gte__(a,b):
		if instanceof(a, String):
			return JS("a.codeUnitAt(0) >= b.codeUnitAt(0)")
		else:
			return JS("a >= b")

