# PythonJS builtins
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"


_PythonJS_UID = 0


with javascript:

	def __object_keys__(ob):
		'''
		notes:
			. Object.keys(ob) will not work because we create PythonJS objects using `Object.create(null)`
			. this is different from Object.keys because it traverses the prototype chain.
		'''
		arr = []
		JS('for (key in ob) { arr.push(key) }')
		return arr

	def __generate_getter__(o, n):
		return lambda : o.__class__.__properties__[ n ]['get']([o],{})
	def __generate_setter__(o, n):
		return lambda v: o.__class__.__properties__[ n ]['set']([o,v],{})


	def __sprintf(fmt, args):
		i = 0
		return JS("fmt.replace(/%((%)|s)/g, function (m) { return m[2] || args[i++] })")

	def create_class(class_name, parents, attrs, props):
		"""Create a PythonScript class"""
		if attrs.__metaclass__:
			metaclass = attrs.__metaclass__
			attrs.__metaclass__ = None
			return metaclass([class_name, parents, attrs])

		klass = Object.create(null)
		klass.__bases__ = parents
		klass.__name__ = class_name
		#klass.__dict__ = attrs
		klass.__properties__ = props
		klass.__attributes__ = attrs
		for key in attrs:
			klass[key] = attrs[key]

		def __call__():
			"""Create a PythonJS object"""
			object = Object.create(null)
			object.__class__ = klass
			#object.__dict__ = {}

			## cache all methods on object ##
			for name in klass.__attributes__:
				if typeof( klass.__attributes__[name] ) == 'function':
					get_attribute( object, name )

			for name in klass.__properties__:
				print 'create-instance property:', name
				desc = {enumerable:True}
				prop = klass.__properties__[ name ]
				if prop['get']:
					## TODO is scope correct that we can not generate the lambda here inside the for loop?
					#lambda : object.__class__.__properties__[ name ]['get']([object],{})
					desc['get'] = __generate_getter__(object, name)
				if prop['set']:
					desc['set'] = __generate_setter__(object, name)

				Object.defineProperty(
					object,
					name,
					desc
				)

			init = get_attribute(object, '__init__')
			if init:
				init.apply(None, arguments)
			return object
		__call__.pythonscript_function = True
		klass.__call__ = __call__
		return klass


def type(ob_or_class_name, bases=None, class_dict=None):
	'''
	type(object) -> the object's type
	type(name, bases, dict) -> a new type  ## broken? - TODO test
	'''
	with javascript:
		if bases is None and class_dict is None:
			return ob_or_class_name.__class__
		else:
			return create_class(ob_or_class_name, bases, class_dict)  ## TODO rename create_class to _pyjs_create_class

def hasattr(ob, attr, method=False):
	with javascript:
		#if method:
		#	return Object.hasOwnProperty.call(ob, attr)
		#elif Object.hasOwnProperty(ob, '__dict__'):
		#	return Object.hasOwnProperty.call(ob.__dict__, attr)
		#else:
		return Object.hasOwnProperty.call(ob, attr)

def getattr(ob, attr, property=False):
	with javascript:
		if property:
			prop = _get_upstream_property( ob.__class__, attr )
			if prop and prop['get']:
				return prop['get']( [ob], {} )
			else:
				print "ERROR: getattr property error", prop
		else:
			return get_attribute(ob, attr)  ## TODO rename to _pyjs_get_attribute

def setattr(ob, attr, value, property=False):
	with javascript:
		if property:
			prop = _get_upstream_property( ob.__class__, attr )
			if prop and prop['set']:
				prop['set']( [ob, value], {} )
			else:
				print "ERROR: setattr property error", prop
		else:
			set_attribute(ob, attr, value)

def issubclass(C, B):
	if C is B:
		return True
	with javascript: bases = C.__bases__  ## js-array
	i = 0
	while i < bases.length:
		if issubclass( bases[i], B ):
			return True
		i += 1
	return False

def isinstance( ob, klass):
	with javascript:
		if ob is None or ob is null:
			return False
		elif not Object.hasOwnProperty.call(ob, '__class__'):
			return False
		ob_class = ob.__class__
	if ob_class is None:
		return False
	else:
		return issubclass( ob_class, klass )



def int(a):
	with javascript:
		if instanceof(a, String):
			return window.parseInt(a)
		else:
			return Math.round(a)

def float(a):
	with javascript:
		if instanceof(a, String):
			return window.parseFloat(a)
		else:
			return a

def round(a, places):
	with javascript:
		b = '' + a
		if b.indexOf('.') == -1:
			return a
		else:
			c = b.split('.')
			x = c[0]
			y = c[1].substring(0, places)
			return parseFloat( x+'.'+y )


def str(s):
	return ''+s

def _setup_str_prototype():
	'''
	Extend JavaScript String.prototype with methods that implement the Python str API.
	The decorator @String.prototype.[name] assigns the function to the prototype,
	and ensures that the special 'this' variable will work.
	'''
	with javascript:

		@String.prototype.__contains__
		def func(a):
			if this.indexOf(a) == -1: return False
			else: return True

		@String.prototype.get
		def func(index):
			return this[ index ]

		@String.prototype.__iter__
		def func(self):
			with python:
				return Iterator(this, 0)

		@String.prototype.__getitem__
		def func(idx):
			return this[ idx ]

		@String.prototype.__len__
		def func():
			return this.length

		@String.prototype.__getslice__
		def func(start, stop, step):
			if stop < 0:
				stop = this.length + stop
			return this.substring(start, stop)

		@String.prototype.splitlines
		def func():
			return this.split('\n')

		@String.prototype.strip
		def func():
			return this.trim()  ## missing in IE8

		@String.prototype.startswith
		def func(a):
			if this.substring(0, a.length) == a:
				return True
			else:
				return False

		@String.prototype.endswith
		def func(a):
			if this.substring(this.length-a.length, this.length) == a:
				return True
			else:
				return False

		@String.prototype.join
		def func(a):
			out = ''
			if instanceof(a, Array):
				arr = a
			else:
				arr = a[...]
			i = 0
			for value in arr:
				out += value
				i += 1
				if i < arr.length:
					out += this
			return out

		@String.prototype.upper
		def func():
			return this.toUpperCase()

		@String.prototype.lower
		def func():
			return this.toLowerCase()

		@String.prototype.index
		def func(a):
			return this.indexOf(a)

		@String.prototype.isdigit
		def func():
			digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
			for char in this:
				if char in digits: pass
				else: return False
			return True

		## TODO - for now these are just dummy functions.
		@String.prototype.decode
		def func(encoding):
			return this
		@String.prototype.encode
		def func(encoding):
			return this


_setup_str_prototype()

def _setup_array_prototype():

	with javascript:

		@Array.prototype.__contains__
		def func(a):
			if this.indexOf(a) == -1: return False
			else: return True

		@Array.prototype.__len__
		def func():
			return this.length

		@Array.prototype.get
		def func(index):
			return this[ index ]

		@Array.prototype.__iter__
		def func(self):
			with python:
				return Iterator(this, 0)

		@Array.prototype.__getslice__
		def func(start, stop, step):
			if stop < 0:
				stop = this.length + stop
			return this.slice(start, stop)


_setup_array_prototype()



def range(num):
	"""Emulates Python's range function"""
	i = 0
	r = list()
	while i < num:
		r.append(i)
		i += 1
	return r


class StopIteration:
	pass


def len(obj):
	return obj.__len__()


def next(obj):
	return obj.next()


def map(func, objs):
	return list( js_object = map(func, objs[...]) )

def min( lst ):
	a = None
	for value in lst:
		if a is None: a = value
		elif value < a: a = value
	return a

def max( lst ):
	a = None
	for value in lst:
		if a is None: a = value
		elif value > a: a = value
	return a

def abs( num ):
	return JS('Math.abs(num)')

def ord( char ):
	return JS('char.charCodeAt(0)')

def chr( num ):
	return JS('String.fromCharCode(num)')

class Iterator:
	## rather than throwing an exception, it could be more optimized to have the iterator set a done flag,
	## and another downside is having the try/catch around this makes errors in in the loop go slient.
	def __init__(self, obj, index):
		self.obj = obj
		self.index = index
		self.length = len(obj)
		self.obj_get = obj.get  ## cache this for speed

	def next(self):
		## slow for looping over something that grows or shrinks while looping,
		## this conforms to standard Python, but it is slow, and probably not often needed.
		index = self.index
		length = len(self.obj)
		if index == length:
			raise StopIteration
		item = self.obj.get(self.index)
		self.index = self.index + 1
		return item

	def next_fast(self):
		with javascript:
			index = self.index
			self.index += 1
			return self.obj_get( [index], {} )


class tuple:
	def __init__(self, js_object=None):
		with javascript:
			arr = []
			self[...] = arr

		if instanceof( js_object, Array ):
			for item in js_object:
				arr.push( item )

		elif js_object:

			if isinstance( js_object, array) or isinstance( js_object, tuple) or isinstance( js_object, list):
				for v in js_object:
					arr.push( v )
			else:
				raise TypeError



	def __getitem__(self, index):
		if index < 0:
			index = self[...].length + index
		with javascript:
			return self[...][index]


	def __iter__(self):
		return Iterator(self, 0)

	def __len__(self):
		with javascript:
			return self[...].length

	def index(self, obj):
		with javascript:
			return self[...].indexOf(obj)

	def count(self, obj):
		with javascript:
			a = 0
			for item in self[...]:
				if item == obj:
					a += 1
			return a


	def get(self, index): ## used by Iterator
		with javascript:
			return self[...][index]

	def __contains__(self, value):
		with javascript:
			if self[...].indexOf(value) == -1:
				return False
			else:
				return True


class list:

	def __init__(self, js_object=None):
		with javascript:
			arr = []
			self[...] = arr

		if instanceof( js_object, Array ):
			for item in js_object:
				arr.push( item )

		elif js_object:

			if isinstance( js_object, array) or isinstance( js_object, tuple) or isinstance( js_object, list):
				for v in js_object:
					arr.push( v )
			else:
				raise TypeError


	def __getitem__(self, index):
		if index < 0:
			index = self[...].length + index
		with javascript:
			return self[...][index]

	def __setitem__(self, index, value):
		with javascript:
			self[...][ index ] = value

	def append(self, obj):
		with javascript:
			self[...].push( obj )

	def extend(self, other):
		for obj in other:
			self.append(obj)

	def insert(self, index, obj):
		with javascript:
			self[...].splice(index, 0, obj)

	def remove(self, obj):
		index = self.index(obj)
		with javascript:
			self[...].splice(index, 1)

	def pop(self):
		with javascript:
			return self[...].pop()

	def index(self, obj):
		with javascript:
			return self[...].indexOf(obj)

	def count(self, obj):
		with javascript:
			a = 0
			for item in self[...]:
				if item == obj:
					a += 1
			return a

	def reverse(self):
		with javascript:
			self[...] = self[...].reverse()

	def shift(self):
		with javascript:
			return self[...].shift()

	def slice(self, start, end):
		with javascript:
			return self[...].slice(start, end)

	def __iter__(self):
		return Iterator(self, 0)

	def get(self, index):
		with javascript:
			return self[...][index]

	def set(self, index, value):
		with javascript:
			self[...][index] = value

	def __len__(self):
		with javascript:
			return self[...].length

	def __contains__(self, value):
		with javascript:
			if self[...].indexOf(value) == -1:
				return False
			else:
				return True

class dict:
	# http://stackoverflow.com/questions/10892322/javascript-hashtable-use-object-key
	# using a function as a key is allowed, but would waste memory because it gets converted to a string
	# http://stackoverflow.com/questions/10858632/are-functions-valid-keys-for-javascript-object-properties
	UID = 0
	def __init__(self, js_object=None):
		with javascript:
			self[...] = {}

		if js_object:
			if JS("js_object instanceof Array"):
				i = 0
				while i < js_object.length:
					JS('var key = js_object[i]["key"]')
					JS('var value = js_object[i]["value"]')
					self.set(key, value)
					i += 1
			else:
				self[...] = js_object


	def get(self, key, _default=None):
		__dict = self[...]
		if JS("typeof(key) === 'object'"):
			JS('var uid = "@"+key.uid') ## gotcha - what if "@undefined" was in __dict ?
			if JS('uid in __dict'):
				return JS('__dict[uid]')
		elif JS("typeof(key) === 'function'"):
			JS('var uid = "@"+key.uid')
			if JS('uid in __dict'):
				return JS('__dict[uid]')
		else:
			if JS('key in __dict'):
				return JS('__dict[key]')

		return _default

	def set(self, key, value):
		global _PythonJS_UID

		__dict = self[...]
		if JS("typeof(key) === 'object'"):
			if JS("key.uid === undefined"):
				uid = _PythonJS_UID
				JS("key.uid = uid")
				_PythonJS_UID += 1
			JS('var uid = key.uid')
			JS('__dict["@"+uid] = value')
		elif JS("typeof(key) === 'function'"):
			if JS("key.uid === undefined"):
				uid = _PythonJS_UID
				JS("key.uid = uid")
				_PythonJS_UID += 1
			JS('var uid = key.uid')
			JS('__dict["@"+uid] = value')
		else:
			JS('__dict[key] = value')

	def __len__(self):
		__dict = self[...]
		return JS('Object.keys(__dict).length')

	def __getitem__(self, key):
		__dict = self[...]
		if JS("typeof(key) === 'object'"):
			JS('var uid = key.uid')
			return JS('__dict["@"+uid]')  ## "@" is needed so that integers can also be used as keys
		elif JS("typeof(key) === 'function'"):
			JS('var uid = key.uid')
			return JS('__dict["@"+uid]')  ## "@" is needed so that integers can also be used as keys
		else:
			return JS('__dict[key]')

	def __setitem__(self, key, value):
		global _PythonJS_UID

		__dict = self[...]
		if JS("typeof(key) === 'object'"):
			if JS("key.uid === undefined"):
				uid = _PythonJS_UID
				JS("key.uid = uid")
				_PythonJS_UID += 1
			JS('var uid = key.uid')
			JS('__dict["@"+uid] = value')
		elif JS("typeof(key) === 'function'"):
			if JS("key.uid === undefined"):
				uid = _PythonJS_UID
				JS("key.uid = uid")
				_PythonJS_UID += 1
			JS('var uid = key.uid')
			JS('__dict["@"+uid] = value')
		else:
			JS('__dict[key] = value')

	def keys(self):
		#__dict = self.js_object
		#__keys = JS('Object.keys(__dict)')  ## the problem with this is that keys are coerced into strings
		#out = list( js_object=__keys )  ## some bug in the translator prevents this
		#out.js_object = __keys  ## this style is deprecated
		#return out
		with javascript:
			arr = Object.keys( self[...] )
		return list( js_object=arr )

	def pop(self, key, d=None):
		v = self.get(key, None)
		if v is None:
			return d
		else:
			js_object = self[...]
			JS("delete js_object[key]")
			return v
		

	def values(self):
		__dict = self[...]
		__keys = JS('Object.keys(__dict)')
		out = list()
		i = 0
		while i < __keys.length:
			out.append( JS('__dict[ __keys[i] ]') )
			i += 1
		return out

	def __contains__(self, value):
		with javascript:
			keys = Object.keys(self[...])  ## the problem with this is that keys are coerced into strings
			if typeof(value) == 'object':
				key = '@'+value.uid
			else:
				key = ''+value  ## convert to string

			if keys.indexOf( key ) == -1:
				return False
			else:
				return True

	def __iter__(self):
		return Iterator(self.keys(), 0)




class array:
	## note that class-level dicts can only be used after the dict class has been defined above,
	## however, we can still not rely on using a dict here because dict creation relies on get_attribute,
	## and get_attribute relies on __NODEJS__ global variable to be set to False when inside NodeJS,
	## to be safe this is changed to use JSObjects
	with javascript:
		typecodes = {
			'c': 1, # char
			'b': 1, # signed char
			'B': 1, # unsigned char
			'u': 2, # unicode
			'h': 2, # signed short
			'H': 2, # unsigned short
			'i': 4, # signed int
			'I': 4, # unsigned int
			'l': 4, # signed long
			'L': 4, # unsigned long
			'f': 4, # float
			'd': 8, # double
			'float32':4,
			'float16':2,
			'float8' :1,

			'int32'  :4,
			'uint32' :4,
			'int16'  :2,
			'uint16' :2,
			'int8'  :1,
			'uint8' :1,
		}
		typecode_names = {
			'c': 'Int8',
			'b': 'Int8',
			'B': 'Uint8',
			'u': 'Uint16',
			'h': 'Int16',
			'H': 'Uint16',
			'i': 'Int32',
			'I': 'Uint32',
			#'l': 'TODO',
			#'L': 'TODO',
			'f': 'Float32',
			'd': 'Float64',

			'float32': 'Float32',
			'float16': 'Int16',
			'float8' : 'Int8',

			'int32'  : 'Int32',
			'uint32' : 'Uint32',
			'int16'  : 'Int16',
			'uint16' : 'Uint16',
			'int8'   : 'Int8',
			'uint8'  : 'Uint8',
		}

	def __init__(self, typecode, initializer=None, little_endian=False):
		self.typecode = typecode
		self.itemsize = self.typecodes[ typecode ]
		self.little_endian = little_endian

		if initializer:
			self.length = len(initializer)
			self.bytes = self.length * self.itemsize

			if self.typecode == 'float8':
				self._scale = max( [abs(min(initializer)), max(initializer)] )
				self._norm_get = self._scale / 127  ## half 8bits-1
				self._norm_set = 1.0 / self._norm_get
			elif self.typecode == 'float16':
				self._scale = max( [abs(min(initializer)), max(initializer)] )
				self._norm_get = self._scale / 32767  ## half 16bits-1
				self._norm_set = 1.0 / self._norm_get

		else:
			self.length = 0
			self.bytes = 0
		
		size = self.bytes
		buff = JS('new ArrayBuffer(size)')
		self.dataview = JS('new DataView(buff)')
		self.buffer = buff
		self.fromlist( initializer )

	def __len__(self):
		return self.length

	def __contains__(self, value):
		#lst = self.to_list()
		#return value in lst  ## this old style is deprecated
		arr = self.to_array()
		with javascript:
			if arr.indexOf(value) == -1: return False
			else: return True

	def __getitem__(self, index):
		step = self.itemsize
		offset = step * index

		dataview = self.dataview
		func_name = 'get'+self.typecode_names[ self.typecode ]
		func = JS('dataview[func_name].bind(dataview)')

		if offset < self.bytes:
			value = JS('func(offset)')
			if self.typecode == 'float8':
				value = value * self._norm_get
			elif self.typecode == 'float16':
				value = value * self._norm_get
			return value
		else:
			raise IndexError

	def __setitem__(self, index, value):
		step = self.itemsize
		if index < 0: index = self.length + index -1  ## TODO fixme
		offset = step * index

		dataview = self.dataview
		func_name = 'set'+self.typecode_names[ self.typecode ]
		func = JS('dataview[func_name].bind(dataview)')

		if offset < self.bytes:
			if self.typecode == 'float8':
				value = value * self._norm_set
			elif self.typecode == 'float16':
				value = value * self._norm_set

			JS('func(offset, value)')
		else:
			raise IndexError

	def __iter__(self):
		return Iterator(self, 0)

	def get(self, index):
		return self[ index ]

	def fromlist(self, lst):
		length = len(lst)
		step = self.itemsize
		typecode = self.typecode
		size = length * step
		dataview = self.dataview
		func_name = 'set'+self.typecode_names[ typecode ]
		func = JS('dataview[func_name].bind(dataview)')
		if size <= self.bytes:
			i = 0; offset = 0
			while i < length:
				item = lst[i]
				if typecode == 'float8':
					item *= self._norm_set
				elif typecode == 'float16':
					item *= self._norm_set

				JS('func(offset,item)')
				offset += step
				i += 1
		else:
			raise TypeError

	def resize(self, length):
		buff = self.buffer
		source = JS('new Uint8Array(buff)')

		new_size = length * self.itemsize
		new_buff = JS('new ArrayBuffer(new_size)')
		target = JS('new Uint8Array(new_buff)')
		JS('target.set(source)')

		self.length = length
		self.bytes = new_size
		self.buffer = new_buff
		self.dataview = JS('new DataView(new_buff)')

	def append(self, value):
		length = self.length
		self.resize( self.length + 1 )
		self[ length ] = value

	def extend(self, lst):  ## TODO optimize
		for value in lst:
			self.append( value )

	def to_array(self):
		arr = JSArray()
		i = 0
		while i < self.length:
			item = self[i]
			JS('arr.push( item )')
			i += 1
		return arr

	def to_list(self):
		return list( js_object=self.to_array() )

	def to_ascii(self):
		string = ''
		arr = self.to_array()
		i = 0; length = arr.length
		while i < length:
			JS('var num = arr[i]')
			JS('var char = String.fromCharCode(num)')
			string += char
			i += 1
		return string


# JSON stuff

with javascript:
	json = {
		'loads': lambda s: JSON.parse(s),
		'dumps': lambda o: JSON.stringify(o)
	}

def _to_pythonjs(json):
	var(jstype, item, output)
	jstype = JS('typeof json')
	if jstype == 'number':
		return json
	if jstype == 'string':
		return json
	if JS("Object.prototype.toString.call(json) === '[object Array]'"):
		output = list()
		raw = list( js_object=json )
		var(append)
		append = output.append
		for item in raw:
			append(_to_pythonjs(item))
		return output
	# else it's a map
	output = dict()
	var(set)
	set = output.set
	keys = list( js_object=JS('Object.keys(json)') )
	for key in keys:
		set(key, _to_pythonjs(JS("json[key]")))
	return output

def json_to_pythonjs(json):
	return _to_pythonjs(JSON.parse(json))

# inverse function

def _to_json(pythonjs):
	if isinstance(pythonjs, list):
		r = JSArray()
		for i in pythonjs:
			r.push(_to_json(i))
	elif isinstance(pythonjs, dict):
		var(r)
		r = JSObject()
		for key in pythonjs.keys():
			value = _to_json(pythonjs.get(key))
			key = _to_json(key)
			with javascript:
				r[key] = value
	else:
		r = pythonjs
	return r


def pythonjs_to_json(pythonjs):
	return JSON.stringify(_to_json(pythonjs))
