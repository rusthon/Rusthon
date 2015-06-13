
inline('IndexError = function(msg) {this.message = msg || "";}; IndexError.prototype = Object.create(Error.prototype); IndexError.prototype.name = "IndexError";')
inline('KeyError   = function(msg) {this.message = msg || "";}; KeyError.prototype = Object.create(Error.prototype); KeyError.prototype.name = "KeyError";')
inline('ValueError = function(msg) {this.message = msg || "";}; ValueError.prototype = Object.create(Error.prototype); ValueError.prototype.name = "ValueError";')
inline('AttributeError = function(msg) {this.message = msg || "";}; AttributeError.prototype = Object.create(Error.prototype);AttributeError.prototype.name = "AttributeError";')
inline('RuntimeError   = function(msg) {this.message = msg || "";}; RuntimeError.prototype = Object.create(Error.prototype);RuntimeError.prototype.name = "RuntimeError";')


## mini fake json library ##
json = {
	'loads': lambda s: JSON.parse(s),
	'dumps': lambda o: JSON.stringify(o)
}

def hasattr(ob, attr):
	## TODO check parent classes for attr, this fails on for methods because those are are on the .prototype ?
	return Object.hasOwnProperty.call(ob, attr)

def len(ob):
	if instanceof(ob, Array):
		return ob.length
	elif __is_typed_array(ob):
		return ob.length
	#elif instanceof(ob, ArrayBuffer):  ## missing in safari
	#	return ob.byteLength
	elif ob.__len__:
		return ob.__len__()
	else: #elif instanceof(ob, Object):
		return Object.keys(ob).length

def func(a):
	if this.indexOf(a) == -1: return False
	else: return True
String.prototype.__contains__ = func

def func(start, stop, step):
	if start is undefined and stop is undefined and step == -1:
		return this.split('').reverse().join('')
	else:
		if stop < 0:
			stop = this.length + stop
		return this.substring(start, stop)
String.prototype.__getslice__ = func

String.prototype.splitlines = lambda : this.split('\n')

String.prototype.strip = lambda : this.trim()  ## missing in IE8

def func(a):
	if this.substring(0, a.length) == a:
		return True
	else:
		return False
String.prototype.startswith = func

def func(a):
	if this.substring(this.length-a.length, this.length) == a:
		return True
	else:
		return False
String.prototype.endswith = func

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
String.prototype.join = func

String.prototype.upper = lambda : this.toUpperCase()

String.prototype.lower = lambda : this.toLowerCase()

def func(a):
	i = this.indexOf(a)
	if i == -1:
		raise ValueError(a + ' - not in string')
	return i
String.prototype.index = func

def func(a):
	if this.indexOf(a) == -1: return False
	else: return True
Array.prototype.__contains__ = func


def func(start, stop, step):
	arr = []

	start = start | 0
	if stop is undefined:
		stop = this.length

	if start < 0:
		start = this.length + start
	if stop < 0:
		stop = this.length + stop

	if typeof(step)=='number':
		if step < 0:
			#step = Math.abs(step)
			i = start
			while i >= 0:
				arr.push( this[i] )
				i += step
			return arr

		else:
			i = start
			n = stop
			while i < n:
				arr.push( this[i] )
				i += step
			return arr

	else:
		i = start
		n = stop
		while i < n:
			#arr[ i ] = this[i]  ## slower in chrome
			arr.push( this[i] )
			i += 1  ## this gets optimized to i++
		return arr
Array.prototype.__getslice__ = func


def func(start, stop, step, items):
	if start is undefined: start = 0
	if stop is undefined: stop = this.length
	arr = [start, stop-start]
	for item in items: arr.push( item )
	this.splice.apply(this, arr )
Array.prototype.__setslice__ = func

def func(item):
	this.push( item )
	return this
Array.prototype.append = func

def func(other):
	a = []
	a.extend(this)
	a.extend(other)
	return a
Array.prototype.__add__ = func

def func(other):
	for obj in other:
		this.push(obj)
	return this
Array.prototype.extend = func

def func(item):
	index = this.indexOf( item )
	this.splice(index, 1)
Array.prototype.remove = func

def func(index, obj):
	if index < 0: index = this.length + index
	this.splice(index, 0, obj)
Array.prototype.insert = func

Array.prototype.index = lambda obj : this.indexOf(obj)

def func(obj):
	a = 0
	for item in this:
		if item is obj:  ## note that `==` will not work here, `===` is required for objects
			a += 1
	return a
Array.prototype.count = func

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
	elif ob and ob.__contains__:
		return ob.__contains__(a)
	elif instanceof(ob, Object) and Object.hasOwnProperty.call(ob, a):
		return True
	else:
		return False

__dom_array_types__ = []
if typeof(NodeList) == 'function':  ## NodeList is only available in browsers
	## minimal dom array types common to allow browsers ##
	__dom_array_types__ = [ NodeList, FileList, DOMStringList, HTMLCollection, SVGNumberList, SVGTransformList]

	## extra dom array types ##
	if typeof(DataTransferItemList) == 'function':  ## missing in NodeWebkit
		__dom_array_types__.push( DataTransferItemList )
	if typeof(HTMLAllCollection) == 'function':     ## missing in Firefox
		__dom_array_types__.push( HTMLAllCollection )
	if typeof(SVGElementInstanceList) == 'function':## missing in Firefox
		__dom_array_types__.push( SVGElementInstanceList )
	if typeof(ClientRectList) == 'function':        ## missing in Firefox-trunk
		__dom_array_types__.push( ClientRectList )

def __is_some_array( ob ):
	if __dom_array_types__.length > 0:
		for t in __dom_array_types__:
			if instanceof(ob, t):
				return True
	return False

def __is_typed_array( ob ):
	#if instanceof( ob, Int8Array ) or instanceof( ob, Uint8Array ):  ## missing in safari
	#	return True
	if instanceof( ob, Int16Array ) or instanceof( ob, Uint16Array ):
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

def __object_keys__(ob):
	'''
	notes:
		. Object.keys(ob) will not work because we create PythonJS objects using `Object.create(null)`
		. this is different from Object.keys because it traverses the prototype chain.
	'''
	arr = []
	inline('for (var key in ob) { arr.push(key) }')
	return arr

def __sprintf(fmt, args):
	## note: '%sXXX%s'.split().length != args.length
	## because `%s` at the start or end will split to empty chunks ##
	if instanceof(args, Array):
		chunks = fmt.split('%s')
		arr = []
		i = 0
		for txt in chunks:
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
			i += 1
		return ''.join(arr)
	else:
		return inline("fmt.replace('%s', args)")



def __jsdict( items ):
	d = inline("{}")
	for item in items:
		key = item[0]
		if instanceof(key, Array):
			key = JSON.stringify(key)
		elif key.__uid__:
			key = key.__uid__
		d[ key ] = item[1]
	return d

def __jsdict_get(ob, key, default_value):
	if instanceof(ob, Object):
		if instanceof(key, Array):
			key = JSON.stringify(key)
		if inline("key in ob"): return ob[key]
		return default_value
	else:  ## PythonJS object instance ##
		## this works because instances from PythonJS are created using Object.create(null) ##
		if default_value is not undefined:
			return JS("ob.get(key, default_value)")
		else:
			return JS("ob.get(key)")

def __jsdict_set(ob, key, value):
	if instanceof(ob, Object):
		if instanceof(key, Array):
			key = JSON.stringify(key)
		ob[ key ] = value
	else:  ## PythonJS object instance ##
		## this works because instances from PythonJS are created using Object.create(null) ##
		JS("ob.set(key,value)")

def __jsdict_keys(ob):
	if instanceof(ob, Object):
		## in the case of tuple keys this would return stringified JSON instead of the original arrays,
		## TODO, should this loop over the keys and convert the json strings back to objects?
		## but then how would we know if a given string was json... special prefix character?
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
			## note: javascript array.pop only pops the end of an array
			if key is undefined:
				return inline("ob.pop()")
			else:
				return ob.splice( key, 1 )[0]
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

def __jsdict_update(ob, other):
	if typeof(ob['update'])=='function':
		return inline('ob.update(other)')
	else:
		for key in __object_keys__(other):
			ob[key]=other[key]


def set(a):
	'''
	This returns an array that is a minimal implementation of set.
	Often sets are used simply to remove duplicate entries from a list, 
	and then it get converted back to a list, it is safe to use set for this.

	The array prototype is overloaded with basic set functions:
		difference
		intersection
		issubset

	'''

	s = []  ## the fake set ##
	for item in a:
		if s.indexOf(item) == -1:
			s.push( item )

	return s


def frozenset(a):
	return set(a)

## set-like features ##

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
Array.prototype.bisect = func

## `-` operator
def func(other):
	f = lambda i: other.indexOf(i)==-1
	return this.filter( f )
Array.prototype.difference = func

## `&` operator
def func(other):
	f = lambda i: other.indexOf(i)!=-1
	return this.filter( f )
Array.prototype.intersection = func


## `<=` operator
def func(other):
	for item in this:
		if other.indexOf(item) == -1:
			return False
	return True
Array.prototype.issubset = func



def int(a):
	a = Math.round(a)
	if isNaN(a):
		raise ValueError('not a number')
	return a



def float(a):
	if typeof(a)=='string':
		if a.lower()=='nan':
			return NaN
		elif a.lower()=='inf':
			return Infinity

	b = Number(a)
	if isNaN(b):
		## invalid strings also convert to NaN, throw error ##
		raise ValueError('can not convert to float: '+a)
	return b

def round(a, places=0):
	b = '' + a
	if b.indexOf('.') == -1:
		return a
	else:
		## this could return NaN with large numbers and large places,
		## TODO check for NaN and instead fallback to `a.toFixed(places)`
		p = Math.pow(10, places)
		return Math.round(a * p) / p

def str(s):
	return ''+s

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



def dir(ob):
	if instanceof(ob, Object):
		return inline("Object.keys( ob )")
	else:
		return __object_keys__(ob)

def __getfast__(ob, attr):
	v = ob[ attr ]
	if v is undefined:
		if ob.__class__:
			v = ob.__class__[attr]
			if v is not undefined:
				return v
		raise AttributeError(attr)
	else:
		return v

def getattr(ob, attr):
	return __getfast__(ob, attr)

def setattr(ob, attr, value):
	ob[attr] = value