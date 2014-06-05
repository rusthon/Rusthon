# PythonJS builtins
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"

pythonjs.configure(runtime_exceptions=False)

_PythonJS_UID = 0

JS('IndexError = function(msg) {this.message = msg || "";}; IndexError.prototype = Object.create(Error.prototype); IndexError.prototype.name = "IndexError";')
JS('KeyError   = function(msg) {this.message = msg || "";}; KeyError.prototype = Object.create(Error.prototype); KeyError.prototype.name = "KeyError";')
JS('ValueError = function(msg) {this.message = msg || "";}; ValueError.prototype = Object.create(Error.prototype); ValueError.prototype.name = "ValueError";')
JS('AttributeError = function(msg) {this.message = msg || "";}; AttributeError.prototype = Object.create(Error.prototype);AttributeError.prototype.name = "AttributeError";')
JS('RuntimeError   = function(msg) {this.message = msg || "";}; RuntimeError.prototype = Object.create(Error.prototype);RuntimeError.prototype.name = "RuntimeError";')

with lowlevel:
	def __getattr__(ob, a ):
		if ob.__getattr__:
			return JS("ob.__getattr__(a)")
		#else:
		#	raise AttributeError(a)

	def __test_if_true__( ob ):
		if ob is True:
			return True
		elif ob is False:
			return False
		elif typeof(ob) == 'string':
			return ob.length != 0
		elif not ob:
			return False
		elif instanceof(ob, Array):
			return ob.length != 0
		elif typeof(ob) == 'function':
			return True
		elif ob.__class__ and ob.__class__ is dict: #isinstance(ob, dict):
			return Object.keys( ob[...] ).length != 0
		elif instanceof(ob, Object):
			return Object.keys(ob).length != 0
		else:
			return True

	def __replace_method(ob, a, b):
		## this is required because string.replace in javascript only replaces the first occurrence
		if typeof(ob) == 'string':
			return ob.split(a).join(b)
		else:
			return ob.replace(a,b)

	def __split_method( ob, delim ):
		## special case because calling string.split() without args its not the same as python,
		## and we do not want to touch the default string.split implementation.
		if typeof(ob) == 'string':
			if delim is undefined:
				return ob.split(' ')
			else:
				return ob.split( delim )
		else:
			if delim is undefined:
				return ob.split()
			else:
				return ob.split( delim )


with javascript:

	def __is_typed_array( ob ):
		if instanceof( ob, Int8Array ) or instanceof( ob, Uint8Array ):
			return True
		elif instanceof( ob, Int16Array ) or instanceof( ob, Uint16Array ):
			return True
		elif instanceof( ob, Int32Array ) or instanceof( ob, Uint32Array ):
			return True
		elif instanceof( ob, Float32Array ) or instanceof( ob, Float64Array ):
			return True
		else:
			return False


	def __js_typed_array( t, a ):
		if t == 'i':
			arr = new( Int32Array(a.length) )

		arr.set( a )
		return arr

	def __contains__( ob, a ):
		t = typeof(ob)
		if t == 'string':
			if ob.indexOf(a) == -1: return False
			else: return True
		elif t == 'number':
			raise TypeError
		elif __is_typed_array(ob):
			for x in ob:
				if x == a:
					return True
			return False
		elif ob.__contains__:
			return ob.__contains__(a)
		elif instanceof(ob, Object) and Object.hasOwnProperty.call(ob, a):
			return True
		else:
			return False

	def __add_op(a, b):
		## 'number' is already checked before this gets called (ternary op)
		## but it can still appear here when called from an inlined lambda
		t = typeof(a)
		if t == 'string' or t == 'number':
			return JS("a+b")
		elif instanceof(a, Array):
			c = []
			c.extend(a)
			c.extend(b)
			return c
		elif a.__add__:
			return a.__add__(b)
		else:
			raise TypeError('invalid objects for addition')

	def __jsdict( items ):
		d = JS("{}")
		for item in items:
			key = item[0]
			if key.__uid__:
				key = key.__uid__
			d[ key ] = item[1]
		return d

	def __jsdict_get(ob, key, default_value):
		if instanceof(ob, Object):
			if JS("key in ob"): return ob[key]
			return default_value
		else:  ## PythonJS object instance ##
			## this works because instances from PythonJS are created using Object.create(null) ##
			if default_value is not undefined:
				return JS("ob.get(key, default_value)")
			else:
				return JS("ob.get(key)")

	def __jsdict_set(ob, key, value):
		if instanceof(ob, Object):
			ob[ key ] = value
		else:  ## PythonJS object instance ##
			## this works because instances from PythonJS are created using Object.create(null) ##
			JS("ob.set(key,value)")

	def __jsdict_keys(ob):
		if instanceof(ob, Object):
			return JS("Object.keys( ob )")
		else:  ## PythonJS object instance ##
			## this works because instances from PythonJS are created using Object.create(null) ##
			return JS("ob.keys()")

	def __jsdict_values(ob):
		if instanceof(ob, Object):
			arr = []
			for key in ob:
				if ob.hasOwnProperty(key):
					value = ob[key]
					arr.push( value )
			return arr
		else:  ## PythonJS object instance ##
			## this works because instances from PythonJS are created using Object.create(null) ##
			return JS("ob.values()")

	def __jsdict_items(ob):
		## `ob.items is None` is for: "self.__dict__.items()" because self.__dict__ is not actually a dict
		if instanceof(ob, Object) or ob.items is undefined:  ## in javascript-mode missing attributes do not raise AttributeError
			arr = []
			for key in ob:
				if Object.hasOwnProperty.call(ob, key):
					value = ob[key]
					arr.push( [key,value] )
			return arr
		else:  ## PythonJS object instance ##
			return JS("ob.items()")

	def __jsdict_pop(ob, key, _default=None):
		if instanceof(ob, Array):
			if ob.length:
				return JS("ob.pop(key)")
			else:
				raise IndexError(key)
		elif instanceof(ob, Object):
			if JS("key in ob"):
				v = ob[key]
				JS("delete ob[key]")
				return v
			elif _default is undefined:
				raise KeyError(key)
			else:
				return _default
		else:  ## PythonJS object instance ##
			## this works because instances from PythonJS are created using Object.create(null) ##
			return JS("ob.pop(key, _default)")

	def __object_keys__(ob):
		'''
		notes:
			. Object.keys(ob) will not work because we create PythonJS objects using `Object.create(null)`
			. this is different from Object.keys because it traverses the prototype chain.
		'''
		arr = []
		JS('for (var key in ob) { arr.push(key) }')
		return arr

	def __bind_property_descriptors__(o, klass):
		for name in klass.__properties__:
			desc = {"enumerable":True}
			prop = klass.__properties__[ name ]
			if prop['get']:
				desc['get'] = __generate_getter__(klass, o, name)
			if prop['set']:
				desc['set'] = __generate_setter__(klass, o, name)

			Object.defineProperty( o, name, desc )

		for base in klass.__bases__:
			__bind_property_descriptors__(o, base)


	def __generate_getter__(klass, o, n):
		return lambda : klass.__properties__[ n ]['get']([o],{})
	def __generate_setter__(klass, o, n):
		return lambda v: klass.__properties__[ n ]['set']([o,v],{})


	def __sprintf(fmt, args):
		## note: '%sXXX%s'.split().length != args.length
		## because `%s` at the start or end will split to empty chunks ##
		if instanceof(args, Array):
			chunks = fmt.split('%s')
			arr = []
			for i,txt in enumerate(chunks):
				arr.append( txt )
				if i >= args.length:
					break
				item = args[i]
				if typeof(item) == 'string':
					arr.append( item )
				elif typeof(item) == 'number':
					arr.append( ''+item )
				else:
					arr.append( Object.prototype.toString.call(item) )
			return ''.join(arr)
		else:
			return fmt.replace('%s', args)

	def __create_class__(class_name, parents, attrs, props):
		"""Create a PythonScript class"""
		#if attrs.__metaclass__:
		#	metaclass = attrs.__metaclass__
		#	attrs.__metaclass__ = None
		#	return metaclass([class_name, parents, attrs])

		klass = Object.create(null)
		klass.__bases__ = parents
		klass.__name__ = class_name
		#klass.__dict__ = attrs
		klass.__unbound_methods__ = Object.create(null)
		klass.__all_method_names__ = []
		klass.__properties__ = props
		klass.__attributes__ = attrs
		for key in attrs:
			if typeof( attrs[key] ) == 'function':
				klass.__all_method_names__.push( key )
				f = attrs[key]
				if hasattr(f, 'is_classmethod') and f.is_classmethod:
					pass
				elif hasattr(f, 'is_staticmethod') and f.is_staticmethod:
					pass
				else:
					klass.__unbound_methods__[key] = attrs[key]

			if key == '__getattribute__': continue
			klass[key] = attrs[key]

		## this is needed for fast lookup of property names in __set__ ##
		klass.__setters__ = []
		klass.__getters__ = []
		for name in klass.__properties__:
			prop = klass.__properties__[name]
			klass.__getters__.push( name )
			if prop['set']:
				klass.__setters__.push( name )
		for base in klass.__bases__:
			Array.prototype.push.apply( klass.__getters__, base.__getters__ )
			Array.prototype.push.apply( klass.__setters__, base.__setters__ )
			Array.prototype.push.apply( klass.__all_method_names__, base.__all_method_names__ )


		def __call__():
			"""Create a PythonJS object"""
			object = Object.create(null)  ## this makes pythonjs object not compatible with things like: Object.hasOwnProperty
			object.__class__ = klass
			object.__dict__ = object
			## we need __dict__ so that __setattr__ can still set attributes using `old-style`: self.__dict__[n]=x
			#Object.defineProperty(
			#	object, 
			#	'__dict__', 
			#	{enumerable:False, value:object, writeable:False, configurable:False}
			#)


			has_getattribute = False
			has_getattr = False
			for name in klass.__all_method_names__:
				if name == '__getattribute__':
					has_getattribute = True
				elif name == '__getattr__':
					has_getattr = True
				else:
					wrapper = __get__(object, name)
					if not wrapper.is_wrapper:
						print 'RUNTIME ERROR: failed to get wrapper for:',name

			## to be safe the getters come after other methods are cached ##
			if has_getattr:
				__get__(object, '__getattr__')

			if has_getattribute:
				__get__(object, '__getattribute__')

			__bind_property_descriptors__(object, klass)

			if object.__init__:
				object.__init__.apply(this, arguments)
				#object.__init__.call(this,args, kwargs)

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

def hasattr(ob, attr):
	## TODO check parent classes for attr
	with javascript:
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
			return __get__(ob, attr)

def setattr(ob, attr, value, property=False):
	with javascript:
		if property:
			prop = _get_upstream_property( ob.__class__, attr )
			if prop and prop['set']:
				prop['set']( [ob, value], {} )
			else:
				print "ERROR: setattr property error", prop
		else:
			__set__(ob, attr, value)

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
		if ob is undefined or ob is null:
			return False
		elif instanceof(ob, Array) and klass is list:
			return True
		#elif klass is dict and instanceof(ob, Object):  ## this is safe because instances created with Object.create(null) are not instances-of Object
		#	if instanceof(ob, Array):
		#		return False
		#	elif ob.__class__:
		#		return False
		#	else:
		#		return True
		elif not Object.hasOwnProperty.call(ob, '__class__'):
			return False

		ob_class = ob.__class__
	if ob_class is undefined:
		return False
	else:
		return issubclass( ob_class, klass )



def int(a):
	with javascript:
		a = Math.round(a)
		if isNaN(a):
			raise ValueError('not a number')
		return a

def float(a):
	with javascript:
		a = Number(a)
		if isNaN(a):
			raise ValueError('not a number')
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
			if index < 0:
				return this[ this.length + index ]
			else:
				return this[ index ]

		@String.prototype.__iter__
		def func(self):
			with python:
				return Iterator(this, 0)

		@String.prototype.__getitem__
		def func(idx):
			if idx < 0:
				return this[ this.length + idx ]
			else:
				return this[ idx ]

		@String.prototype.__len__
		def func():
			return this.length

		@String.prototype.__getslice__
		def func(start, stop, step):
			if start is undefined and stop is undefined and step == -1:
				return this.split('').reverse().join('')
			else:
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
			i = this.indexOf(a)
			if i == -1:
				raise ValueError(a + ' - not in string')
			return i

		@String.prototype.find
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

		@String.prototype.format
		def func(fmt):
			r = this
			keys = Object.keys(fmt)
			for key in keys:
				r = r.split(key).join(fmt[key])
			r = r.split('{').join('').split('}').join('')
			return r


_setup_str_prototype()

def _setup_array_prototype():

	with javascript:
		@Array.prototype.jsify
		def func():
			i = 0
			while i < this.length:
				item = this[ i ]
				if typeof(item) == 'object':
					if item.jsify:
						this[ i ] = item.jsify()
				i += 1
			return this

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

		@Array.prototype.__getitem__
		def __getitem__(index):
			if index < 0: index = this.length + index
			return this[index]

		@Array.prototype.__setitem__
		def __setitem__(index, value):
			if index < 0: index = this.length + index
			this[ index ] = value

		@Array.prototype.__iter__
		def func():
			with python:
				return Iterator(this, 0)

		@Array.prototype.__getslice__
		def func(start, stop, step):
			if start is undefined and stop is undefined:
				arr = []
				i = 0
				while i < this.length:
					arr.push( this[i] )
					i += step
				return arr
			else:
				if stop < 0:
					stop = this.length + stop
				return this.slice(start, stop)

		@Array.prototype.append
		def func(item):
			this.push( item )
			return this

		@Array.prototype.extend
		def extend(other):
			for obj in other:
				this.push(obj)
			return this

		@Array.prototype.remove
		def func(item):
			index = this.indexOf( item )
			this.splice(index, 1)

		@Array.prototype.insert
		def insert(index, obj):
			if index < 0: index = this.length + index
			this.splice(index, 0, obj)

		@Array.prototype.index
		def index(obj):
			return this.indexOf(obj)

		@Array.prototype.count
		def count(obj):
			a = 0
			for item in this:
				if item is obj:  ## note that `==` will not work here, `===` is required for objects
					a += 1
			return a


		## set-like features ##

		@Array.prototype.bisect
		def func(x, low, high):
			if low is undefined: low = 0
			if high is undefined: high = this.length
			while low < high:
				a = low+high
				mid = Math.floor(a/2)
				if x < this[mid]:
					high = mid
				else:
					low = mid + 1
			return low

		## `-` operator
		@Array.prototype.difference
		def func(other):
			f = lambda i: other.indexOf(i)==-1
			return this.filter( f )
		## `&` operator
		@Array.prototype.intersection
		def func(other):
			f = lambda i: other.indexOf(i)!=-1
			return this.filter( f )
		## `<=` operator
		@Array.prototype.issubset
		def func(other):
			for item in this:
				if other.indexOf(item) == -1:
					return False
			return True

_setup_array_prototype()



def _setup_nodelist_prototype():

	with javascript:

		@NodeList.prototype.__contains__
		def func(a):
			if this.indexOf(a) == -1: return False
			else: return True

		@NodeList.prototype.__len__
		def func():
			return this.length

		@NodeList.prototype.get
		def func(index):
			return this[ index ]

		@NodeList.prototype.__getitem__
		def __getitem__(index):
			if index < 0: index = this.length + index
			return this[index]

		@NodeList.prototype.__setitem__
		def __setitem__(index, value):
			if index < 0: index = this.length + index
			this[ index ] = value

		@NodeList.prototype.__iter__
		def func():
			with python:
				return Iterator(this, 0)

		@NodeList.prototype.index
		def index(obj):
			return this.indexOf(obj)


if __NODEJS__ == False and __WEBWORKER__ == False:
	_setup_nodelist_prototype()


def bisect(a, x, low=None, high=None):
	#if isinstance(a, list):
	#	return a[...].bisect(x, low, high)
	return a.bisect(x, low, high)


def range(num, stop, step):
	"""Emulates Python's range function"""
	if stop is not undefined:
		i = num
		num = stop
	else:
		i = 0
	if step is undefined:
		step = 1
	with javascript:
		arr = []
		while i < num:
			arr.push(i)
			i += step
	return arr

def xrange(num, stop, step):
	return range(num, stop, step)

def sum( arr ):
	a = 0
	for b in arr:
		a += b
	return a

class StopIteration:  ## DEPRECATED
	pass


def len(ob):
	with javascript:
		if instanceof(ob, Array):
			return ob.length
		elif __is_typed_array(ob):
			return ob.length
		elif instanceof(ob, ArrayBuffer):
			return ob.byteLength
		elif instanceof(ob, Object):
			return Object.keys(ob).length
		else:
			with python:
				return ob.__len__()


def next(obj):
	return obj.next()


def map(func, objs):
	with javascript: arr = []
	for ob in objs:
		v = func(ob)
		with javascript:
			arr.push( v )
	return arr

def filter(func, objs):
	with javascript: arr = []
	for ob in objs:
		if func( ob ):
			with javascript:
				arr.push( ob )
	return arr


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

with javascript:
	class __ArrayIterator:
		def __init__(self, arr, index):
			self.arr = arr
			self.index = index
			self.length = arr.length

		def next(self):
			index = self.index
			self.index += 1
			arr = self.arr
			return JS('arr[index]')


class Iterator:
	## rather than throwing an exception, it could be more optimized to have the iterator set a done flag,
	## and another downside is having the try/catch around this makes errors in in the loop go slient.
	def __init__(self, obj, index):
		self.obj = obj
		self.index = index
		self.length = len(obj)
		self.obj_get = obj.get  ## cache this for speed

	def next(self):
		with javascript:
			index = self.index
			self.index += 1
			return self.obj_get( [index], {} )


def tuple(a):
	## TODO tuple needs a solution for dict keys
	with javascript:
		if Object.keys(arguments).length == 0: #arguments.length == 0:
			return []
		elif instanceof(a, Array):
			return a.slice()
		elif typeof(a) == 'string':
			return a.split('')
		else:
			print a
			print arguments
			raise TypeError



def list(a):
	with javascript:
		if Object.keys(arguments).length == 0: #arguments.length == 0:
			return []
		elif instanceof(a, Array):
			return a.slice()
		elif typeof(a) == 'string':
			return a.split('')
		else:
			print a
			print arguments
			raise TypeError




class dict:
	# http://stackoverflow.com/questions/10892322/javascript-hashtable-use-object-key
	# using a function as a key is allowed, but would waste memory because it gets converted to a string
	# http://stackoverflow.com/questions/10858632/are-functions-valid-keys-for-javascript-object-properties
	def __init__(self, js_object=None, pointer=None):
		with javascript:
			self[...] = {}

		if pointer is not None:
			self[...] = pointer

		elif js_object:
			ob = js_object
			if instanceof(ob, Array):
				for o in ob:
					if instanceof(o, Array):
						self.__setitem__( o[0], o[1] )
					else:
						self.__setitem__( o['key'], o['value'] )
			elif isinstance(ob, dict):
				for key in ob.keys():
					value = ob[ key ]
					self.__setitem__( key, value )
			else:
				print 'ERROR init dict from:', js_object
				raise TypeError

	def jsify(self):
		#keys = Object.keys( self[...] )  ## TODO check how this got broken, this should always be a low-level object?
		keys = __object_keys__( self[...] )
		for key in keys:
			value = self[...][key]
			if typeof(value) == 'object':
				if hasattr(value, 'jsify'):
					self[...][key] = value.jsify()
			elif typeof(value) == 'function':
				raise RuntimeError("can not jsify function")
		return self[...]

	def copy(self):
		return dict( self )

	def clear(self):
		with javascript:
			self[...] = {}

	def has_key(self, key):
		__dict = self[...]
		if JS("typeof(key) === 'object' || typeof(key) === 'function'"):
			# Test undefined because it can be in the dict
			key = key.__uid__

		if JS("key in __dict"):
			return True
		else:
			return False

	def update(self, other):
		for key in other:
			self.__setitem__( key, other[key] )

	def items(self):
		arr = []
		for key in self.keys():
			arr.append( [key, self[key]] )
		return arr

	def get(self, key, _default=None):
		try:
			return self[key]
		except:
			return _default

	def set(self, key, value):
		self.__setitem__(key, value)

	def __len__(self):
		__dict = self[...]
		return JS('Object.keys(__dict).length')

	def __getitem__(self, key):
		'''
		notes:
			. '4' and 4 are the same key
			. it is possible that the translator mistakes a javascript-object for a dict and inlines this function,
			  that is why below we return the key in self if __dict is undefined.
		'''
		__dict = self[...]
		if JS("typeof(key) === 'object' || typeof(key) === 'function'"):
			# Test undefined because it can be in the dict
			if JS("key.__uid__ && key.__uid__ in __dict"):
				return JS('__dict[key.__uid__]')
			raise KeyError(key)

		# Tested after in order to not convert functions to strings.
		# The slow down is negligible
		if __dict and JS("key in __dict"):
			return JS('__dict[key]')

		raise KeyError(key)

	def __setitem__(self, key, value):
		__dict = self[...]
		if JS("typeof(key) === 'object' || typeof(key) === 'function'"):
			if JS("key.__uid__ === undefined"):
				# "￼" is needed so that integers can also be
				# used as keys
				JS(u"key.__uid__ = '￼' + _PythonJS_UID++")
			JS('__dict[key.__uid__] = value')
		else:
			JS('__dict[key] = value')

	def keys(self):
		with javascript:
			return Object.keys( self[...] )

	def pop(self, key, d=None):
		v = self.get(key, None)
		if v is None:
			return d
		else:
			js_object = self[...]
			JS("delete js_object[key]")
			return v

	def values(self):
		with javascript:
			keys = Object.keys( self[...] )
			out = []
			for key in keys:
				out.push( self[...][key] )
			return out

	def __contains__(self, value):
		try:
			self[value]
			return True
		except:
			return False

	def __iter__(self):
		return Iterator(self.keys(), 0)



def set(a):
	'''
	This returns an array that is a minimal implementation of set.
	Often sets are used simply to remove duplicate entries from a list, 
	and then it get converted back to a list, it is safe to use fastset for this.

	The array prototype is overloaded with basic set functions:
		difference
		intersection
		issubset

	Note: sets in Python are not subscriptable, but can be iterated over.

	Python docs say that set are unordered, some programs may rely on this disorder
	for randomness, for sets of integers we emulate the unorder only uppon initalization 
	of the set, by masking the value by bits-1. Python implements sets starting with an 
	array of length 8, and mask of 7, if set length grows to 6 (3/4th), then it allocates 
	a new array of length 32 and mask of 31.  This is only emulated for arrays of 
	integers up to an array length of 1536.

	'''
	with javascript:
		if isinstance(a, list): a = a[...]
		hashtable = null
		if a.length <= 1536:
			hashtable = {}
			keys = []
			if a.length < 6:  ## hash array length 8
				mask = 7
			elif a.length < 22: ## 32
				mask = 31
			elif a.length < 86: ## 128
				mask = 127
			elif a.length < 342: ## 512
				mask = 511
			else: 				## 2048
				mask = 2047

		fallback = False
		if hashtable:
			for b in a:
				if typeof(b,'number') and b is (b|0):  ## set if integer
					key = b & mask
					hashtable[ key ] = b
					keys.push( key )
				else:
					fallback = True
					break

		else:
			fallback = True

		s = []

		if fallback:
			for item in a:
				if s.indexOf(item) == -1:
					s.push( item )
		else:
			keys.sort()
			for key in keys:
				s.push( hashtable[key] )

	return s


def frozenset(a):
	return set(a)




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
			raise IndexError(index)

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
			raise IndexError(index)

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
		return self.to_array()

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


## file IO ##
class file:
	'''
	TODO, support multiple read/writes.  Currently this just reads all data,
	and writes all data.
	'''
	def __init__(self, path, flags):
		self.path = path

		if flags == 'rb':
			self.flags = 'r'
			self.binary = True
		elif flags == 'wb':
			self.flags = 'w'
			self.binary = True
		else:
			self.flags = flags
			self.binary = False

		self.flags = flags

	def read(self, binary=False):
		_fs = require('fs')
		path = self.path
		with javascript:
			if binary or self.binary:
				return _fs.readFileSync( path )
			else:
				return _fs.readFileSync( path, {'encoding':'utf8'} )

	def write(self, data, binary=False):
		_fs = require('fs')
		path = self.path
		with javascript:
			if binary or self.binary:
				_fs.writeFileSync( path, data )
			else:
				_fs.writeFileSync( path, data, {'encoding':'utf8'} )

	def close(self):
		pass

def __open__( path, mode=None):  ## this can not be named `open` because it replaces `window.open`
	return file( path, mode )


with javascript:

	## mini json library ##
	json = {
		'loads': lambda s: JSON.parse(s),
		'dumps': lambda o: JSON.stringify(o)
	}


	def __get_other_workers_with_shared_arg( worker, ob ):
		a = []
		for b in threading.workers:
			other = b['worker']
			args = b['args']
			if other is not worker:
				for arg in args:
					if arg is ob:
						if other not in a:
							a.append( other )
		return a

	threading = {'workers': [] }


	def __start_new_thread(f, args):
		worker = new(Worker(f))
		worker.__uid__ = len( threading.workers )
		threading.workers.append( {'worker':worker,'args':args} )

		def func(event):
			#print('got signal from thread')
			#print(event.data)
			if event.data.type == 'terminate':
				worker.terminate()
			elif event.data.type == 'call':
				__module__[ event.data.function ].apply(null, event.data.args)

			elif event.data.type == 'append':
				#print('got append event')
				a = args[ event.data.argindex ]
				a.push( event.data.value )
				for other in __get_other_workers_with_shared_arg(worker, a):
					other.postMessage( {'type':'append', 'argindex':event.data.argindex, 'value':event.data.value} )

			elif event.data.type == '__setitem__':
				#print('got __setitem__ event')
				a = args[ event.data.argindex ]
				value = event.data.value
				if a.__setitem__:
					a.__setitem__(event.data.index, value)
				else:
					a[event.data.index] = value

				for other in __get_other_workers_with_shared_arg(worker, a):
					#print('relay __setitem__')
					other.postMessage( {'type':'__setitem__', 'argindex':event.data.argindex, 'key':event.data.index, 'value':event.data.value} )


			else:
				raise RuntimeError('unknown event')

		worker.onmessage = func
		jsargs = []
		for i,arg in enumerate(args):
			if arg.jsify:
				jsargs.append( arg.jsify() )
			else:
				jsargs.append( arg )


			if instanceof(arg, Array):
				__gen_worker_append(worker, arg, i)

		worker.postMessage( {'type':'execute', 'args':jsargs} )
		return worker


	def __gen_worker_append(worker, ob, index):
		def append(item):
			#print('posting to thread - append')
			worker.postMessage( {'type':'append', 'argindex':index, 'value':item} )
			ob.push( item )
		Object.defineProperty(ob, "append", {'enumerable':False, 'value':append, 'writeable':True, 'configurable':True})

	######## webworker client #########

	def __webworker_wrap(ob, argindex):
		if instanceof(ob, Array):
			#ob.__argindex__ = argindex

			def func(index, item):
				#print('posting to parent setitem')
				postMessage({'type':'__setitem__', 'index':index, 'value':item, 'argindex':argindex})
				Array.prototype.__setitem__.call(ob, index, item)

			## this can raise RangeError recursive overflow if the worker entry point is a recursive function
			Object.defineProperty(ob, "__setitem__", {"enumerable":False, "value":func, "writeable":True, "configurable":True})
			#ob.__setitem__ =func

			def func(item):
				#print('posting to parent append')
				postMessage({'type':'append', 'value':item, 'argindex':argindex})
				Array.prototype.push.call(ob, item)
			Object.defineProperty(ob, "append", {"enumerable":False, "value":func, "writeable":True, "configurable":True})
			#ob.append = func
		elif typeof(ob) == 'object':
			def func(key, item):
				#print('posting to parent setitem object')
				postMessage({'type':'__setitem__', 'index':key, 'value':item, 'argindex':argindex})
				ob[ key ] = item
			#ob.__setitem__ = func
			Object.defineProperty(ob, "__setitem__", {"enumerable":False, "value":func, "writeable":True, "configurable":True})

		return ob




