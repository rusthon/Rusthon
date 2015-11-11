inline('var __$UID$__ = 1')  ## used for object hashes, gets incremented by object constructors

inline('IndexError = function(msg) {this.message = msg || "";}; IndexError.prototype = Object.create(Error.prototype); IndexError.prototype.name = "IndexError";')
inline('KeyError   = function(msg) {this.message = msg || "";}; KeyError.prototype = Object.create(Error.prototype); KeyError.prototype.name = "KeyError";')
inline('ValueError = function(msg) {this.message = msg || "";}; ValueError.prototype = Object.create(Error.prototype); ValueError.prototype.name = "ValueError";')
inline('AttributeError = function(msg) {this.message = msg || "";}; AttributeError.prototype = Object.create(Error.prototype);AttributeError.prototype.name = "AttributeError";')
inline('RuntimeError   = function(msg) {this.message = msg || "";}; RuntimeError.prototype = Object.create(Error.prototype);RuntimeError.prototype.name = "RuntimeError";')
inline('WebWorkerError = function(msg) {this.message = msg || "";}; WebWorkerError.prototype = Object.create(Error.prototype);WebWorkerError.prototype.name = "WebWorkerError";')
inline('TypeError = function(msg) {this.message = msg || "";}; TypeError.prototype = Object.create(Error.prototype);TypeError.prototype.name = "TypeError";')

def __invalid_call__(msg, args):
	print '[INVALID CALL ARGUMENTS]'
	if args is not undefined:
		for i in range(args.length):
			print '	argument:' + i + ' -> ' + args[i]
	raise RuntimeError(msg)

def __array_fill__(arr, items):
	for i in range(items.length):
		arr[i] = items[i]
	return arr

def __set_timeout(func, seconds):
	## note: 10ms is the smallest possible time for setTimeout/Interval
	ms = seconds * 1000
	id = setTimeout( func, ms )
	func._timeout_id = id
	return func

def __set_interval(func, seconds):
	ms = seconds * 1000
	id = setInterval( func, ms )
	func._interval_id = id
	return func


@unicode('𝑰𝒔𝑰𝒏𝒔𝒕𝒂𝒏𝒄𝒆')
def isinstance( ob, klass):
	if ob is undefined or ob is null:
		return False
	elif typeof(klass) is 'string':
		T = typeof( ob )
		if T == 'number':
			if klass == 'int' or klass == '𝑰𝒏𝒕𝒆𝒈𝒆𝒓':
				return True
			elif klass == 'float' or klass == '𝑭𝒍𝒐𝒂𝒕':
				return True
			else:
				return False
		elif T == 'string':
			if klass == 'string' or klass == 'str' or klass == '𝑺𝒕𝒓𝒊𝒏𝒈':
				return True
			else:
				return False
		elif klass == 'Array' or klass == 'list' or klass == '𝑳𝒊𝒔𝒕':
			if instanceof(ob, Array):
				return True
			else:
				return False
		elif ob.__class__:
			if ob.__class__.__name__ == klass:
				return True
			else:
				return False
		else:
			return False


	elif instanceof(ob, Array):
		if klass is list:
			return True
		elif klass is Array:
			return True
		else:
			return False

	elif instanceof(ob, klass):
		return True

	elif ob.__class__:  ## TODO check typeof
		return issubclass(ob.__class__, klass)

	elif typeof(ob)=='number':
		if klass is int and ob.toString().isdigit():
			return True
		elif klass is float:  ## must always be true because `0.0` becomes `0`
			return True
		else:
			return False
	elif typeof(ob)=='string':
		if klass is str or klass is string:
			return True
		else:
			return False
	else:
		return False

@unicode('𝑰𝒔𝑺𝒖𝒃𝒄𝒍𝒂𝒔𝒔')
def issubclass(C, B):
	if C is B:
		return True
	elif C.__bases__:
		for base in C.__bases__:
			#if base is undefined:
			#	print C.__bases__
			#	#print __n0
			#	raise RuntimeError(C.__bases__)
			if issubclass(base, B):
				return True
	return False

@unicode('𝑳𝒆𝒏𝒈𝒕𝒉')
def len(ob):
	if instanceof(ob, Array):
		return ob.length
	elif __is_typed_array(ob):
		return ob.length
	elif ob.__len__:
		return ob.__len__()
	elif isNaN(ob):
		raise RuntimeError('calling `len` with NaN in invalid')
	elif typeof(ob)=='number':
		raise RuntimeError('calling `len` on a number is invalid')
	else:  ## let this fail at runtime if ob is not an object
		return Object.keys(ob).length

def __htmldoc_rightarrow__(arg):
	if arg.startswith('#'):
		return this.getElementById(arg[1:])
	else:
		return this.createElement(arg)

def __htmlelement_rightarrow__():
	if arguments.length==0:
		while this.childNodes.length:
			this.removeChild( this.firstChild )
	else:
		for item in arguments:
			T = typeof(item)
			if instanceof(item, HTMLElement):
				this.appendChild( item )
			elif instanceof(item, Text):  ## a text node create by `document.createTextNode`
				this.appendChild( item )
			elif T=='string':
				this.appendChild( document.createTextNode(item) )
			elif T=='function':
				raise RuntimeError('HTMLElement->(lambda function) is invalid')
			elif T=='object':
				## could be a DOM node from another document/iframe
				if item.nodeType:
					if item.nodeType==Node.TEXT_NODE:
						this.appendChild(item)
					elif item.nodeType==Node.ELEMENT_NODE:
						this.appendChild(item)
					else:
						raise RuntimeError('HTMLElement unknown node type')
				else:
					for key in item.keys():
						this.setAttribute(key, item[key])
			else:
				raise RuntimeError('HTMLElement->(invalid type): '+ item)

	return this


# becomes function `ᐅ` note: from unicode unified can-ab
def __right_arrow__():
	ob = arguments[0]
	args = []
	for i in range(1, arguments.length):
		args.push( arguments[i] )

	if ob.__right_arrow__:
		return ob.__right_arrow__.apply(ob, args)
	elif ob.nodeType:
		switch ob.nodeType:
			case document.DOCUMENT_NODE:
				ob.__right_arrow__ = __htmldoc_rightarrow__.bind(ob)
			case document.ELEMENT_NODE:
				ob.__right_arrow__ = __htmlelement_rightarrow__.bind(ob)
		return ob.__right_arrow__.apply(ob, args)
	else:
		raise RuntimeError('invalid use of ->')

if HTMLElement is not undefined:
	HTMLElement.prototype.__right_arrow__  = __htmlelement_rightarrow__
	HTMLDocument.prototype.__right_arrow__ = __htmldoc_rightarrow__


# the unicode decorator is used in the global namespace to define
# a mapping from the function name to the unicode version of the name.
# the user is able to then define their own unicode scripting language,
# that can have greater readablity, and will not having naming collisions
# with external javascript libraries, because nobody has made js libraries
# yet that use unicode variable names.
@unicode('𝑫𝒊𝒄𝒕')
def dict( d, copy=False, keytype=None, valuetype=None, iterable=None ):
	## note: the chrome debugger will still show these hidden attributes
	## when printing the object in the console, even when `enumerable` is false.
	if instanceof(d, Array):
		pairs = d
		d = inline('{}')
		for pair in pairs:
			if keytype is not None:
				if not isinstance(pair[0], keytype):
					msg = 'INVALID KEY-TYPE: `%s` - expected type `%s`' %(typeof(pair[0]), keytype)
					raise TypeError(msg)
			if valuetype is not None:
				if not isinstance(pair[1], valuetype):
					msg = 'INVALID VALUE-TYPE: `%s` - expected type `%s`' %(typeof(pair[1]), valuetype)
					raise TypeError(msg)

			inline('d[ pair[0] ] = pair[1]')

	if iterable is not None:
		for pair in iterable:
			if keytype is not None:
				if not isinstance(pair[0], keytype):
					msg = 'INVALID KEY-TYPE: `%s` - expected type `%s`' %(typeof(pair[0]), keytype)
					raise TypeError(msg)

			if valuetype is not None:
				if not isinstance(pair[1], valuetype):
					msg = 'INVALID VALUE-TYPE: `%s` - expected type `%s`' %(typeof(pair[1]), valuetype)
					raise TypeError(msg)

			inline('d[ pair[0] ] = pair[1]')



	Object.defineProperty(d, '__class__', value=dict, enumerable=False)

	if keytype is not None or valuetype is not None:

		if keytype is not None:
			Object.defineProperty(d, '__keytype__', value=keytype, enumerable=False)
		if valuetype is not None:
			Object.defineProperty(d, '__valuetype__', value=valuetype, enumerable=False)

		def __setitem__(key, value):
			if keytype is not None:
				if not isinstance(key, keytype):
					print 'TypeError-KEY:' + key
					msg = 'INVALID KEY-TYPE: `%s` - expected type `%s`' %(typeof(key), keytype)
					raise TypeError(msg)

			if valuetype is not None:
				if not isinstance(value, valuetype):
					print 'TypeError-VALUE:' + value
					msg = 'INVALID VALUE-TYPE: `%s` - expected type `%s`' %(typeof(value), valuetype)
					raise TypeError(msg)

			inline('d[key] = value')

		Object.defineProperty(d, '__setitem__', value=__setitem__, enumerable=False)


	if not copy:
		return d
	else:
		raise RuntimeError('TODO dict(copyme)')

dict.__name__ = 'dict'

@unicode('𝑷𝒓𝒊𝒏𝒕')
def __print__():
	for a in arguments:
		console.log(a)

def __object_keys__(ob):
	'''
	notes:
		. promotes keys to integers, also works on external objects coming from js.
		. Object.keys(ob) traverses the full prototype chain.
	'''
	arr = []
	if ob.__keytype__ is not undefined:
		if ob.__keytype__ == 'int':
			inline('for (var key in ob) {arr.push(int(key))}')
		else:
			inline('for (var key in ob) {arr.push(key)}')
		return arr
	else:
		## this could be faster using maybe using this trick?
		## (JSON.stringify(Object.keys(ob)).replace('"','').replace(',', '')[1:-1] + '').isdigit()
		isdigits = False
		test = 0
		inline('for (var key in ob) { arr.push(key); if (key.isdigit()) {test += 1;} }')
		isdigits = test == arr.length

		if isdigits:
			iarr = []
			for key in arr:
				iarr.push( int(key) )
			return iarr
		else:
			return arr

## this is not called ObjectKeys because this is used for `ob.keys()`
## where `ob` could be a regular object, or python dict.
@unicode('𝑲𝒆𝒚𝒔')
def __jsdict_keys(ob):
	if ob.__class__ is not undefined:  ## assume this is a PythonJS class and user defined `keys` method
		if ob.__class__ is dict:
			if ob.__keytype__ is not undefined and ob.__keytype__ == 'int':
				return JSON.parse(
					'[' + 
					inline("Object.keys( ob ).toString()").replace('"','')
					+ ']'
				)
			else:
				return inline("Object.keys( ob )")
		else:
			return inline("ob.keys()")
	elif instanceof(ob, Object):
		## what is a good way to know when this an external class instance with a method `keys`
		## versus an object where `keys` is is a function?
		## this only breaks with classes from external js libraries?
		if ob.keys is not undefined and isinstance(ob.keys, Function):
			return inline("ob.keys()")
		else:
			return inline("Object.keys( ob )")
	else:  ## rare case ##
		## something without a prototype - created using Object.create(null) ##
		return inline("ob.keys()")


@bind(Function.prototype.redefine)
def __redef_function(src):
	if isinstance(src, Function):
		this.__redef = src
		this.__recompile = undefined
	else:
		this.__recompile = src
#Function.prototype.redefine = __redef_function


## mini fake json library ##
json = {
	'loads': lambda s: JSON.parse(s),
	'dumps': lambda o: JSON.stringify(o)
}

def hasattr(ob, attr):
	if Object.hasOwnProperty.call(ob, attr):
		return True
	elif ob[attr] is not undefined:
		return True
	else:
		return False

@unicode('𝑳𝒊𝒔𝒕')
def list(ob):
	a = []
	if ob is not undefined:
		if isinstance(ob, string):
			for i in range(ob.length):
				a.push(ob[i])
		else:
			for e in ob:
				a.push(e)
	return a

@unicode('𝑻𝒖𝒑𝒍𝒆')
def tuple(ob):
	a = []
	if ob is not undefined:
		for e in ob:
			a.push(e)
	return a


@bind(String.prototype.__add__)
def __string_add(a):
	return this + a

@bind(String.prototype.__mul__)
def __string_multiply(a):
	out = ''
	for i in range(a): out += this
	return out

@bind(String.prototype.__contains__)
def __string_contains(a):
	if this.indexOf(a) == -1: return False
	else: return True

@bind(String.prototype.__getslice__)
def __string_slice(start, stop, step):
	if start is undefined and stop is undefined and step == -1:
		return this.split('').reverse().join('')
	else:
		if stop < 0:
			stop = this.length + stop
		return this.substring(start, stop)

@bind(String.prototype.__getslice_lowerstep__)
def __string_getslice_lowerstep__(start, step):
	return this.__getslice__(start, undefined, step)

String.prototype.splitlines = lambda : this.split('\n')

String.prototype.strip = lambda : this.trim()  ## missing in IE8

String.prototype.__len__ = lambda : this.length

@bind(String.prototype.startswith)
def __string_startswith(a):
	if this.substring(0, a.length) == a:
		return True
	else:
		return False

@bind(String.prototype.endswith)
def __string_endswith(a):
	if this.substring(this.length-a.length, this.length) == a:
		return True
	else:
		return False

@bind(String.prototype.join)
def __string_join(arr):
	out = ''
	i = 0
	for value in arr:
		out += value
		i += 1
		if i < arr.length:
			out += this
	return out

String.prototype.upper = lambda : this.toUpperCase()

String.prototype.lower = lambda : this.toLowerCase()

@bind(Number.prototype.__sub__)
def __number_sub(other):
	return this - other
@bind(Number.prototype.__add__)
def __number_add(other):
	return this + other
@bind(Number.prototype.__mul__)
def __number_mul(other):
	return this * other
@bind(Number.prototype.__div__)
def __number_div(other):
	return this / other
@bind(Number.prototype.__mod__)
def __number_mod(other):
	return this % other


@bind(String.prototype.index)
def __string_index(a):
	i = this.indexOf(a)
	if i == -1:
		raise ValueError(a + ' - not in string')
	return i

@bind(Array.prototype.equals)  ## non standard
def __array_equals(a):
	return JSON.stringify(this) == JSON.stringify(a)


@bind(Array.prototype.copy)    ## non standard in python, used by `myarr[:]`
def __array_copy():
	#return [].concat(this)
	#return this.slice()
	a = new Array(this.length)
	for i in range(this.length):
		a[i]=this[i]
	return a

#def iter(arr):
#	if instanceof(arr, Array):
#		return arr
#	elif typeof(arr)=='string':
#		return arr
#	elif __is_some_array(arr):
#		return arr
#	else:
#		return inline("Object.keys(arr)")

@bind(Array.prototype.__contains__)
def __array_contains(a):
	if this.indexOf(a) == -1: return False
	else: return True

@bind(Array.prototype.__getslice_lowerstep__)
def __array_getslice_lowerstep__(start, step):
	start = start | 0
	arr = []
	if step < 0:
		while start >= 0:
			arr.push( this[start] )
			start += step
	else:
		n = this.length
		while start < n:
			arr.push( this[start] )
			start += step

	return arr


@bind(Array.prototype.__getslice__)
def __array_getslice(start, stop, step):
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


@bind(Array.prototype.__setslice__)
def __array_setslice(start, stop, step, items):  ## TODO step
	if start is undefined: start = 0
	if stop is undefined: stop = this.length
	#arr = [start, stop-start]
	#for i in range(items.length):
	#	arr.push( items[i] )
	#this.splice.apply(this, arr )

	itemslen = items.length
	thislen = this.length
	remove  = stop-start
	newlen  = itemslen+thislen-remove
	if thislen < newlen:
		offset = newlen-thislen
		this.length = newlen
		## move elements in place forward
		i = thislen-1
		while i >= stop:
			this[ i+offset ] = this[i]
			i -= 1
		for j in range(itemslen):
			this[j+start] = items[j]

	elif thislen == newlen:
		i = 0
		for j in range(start, stop):
			this[j] = items[i]
			i += 1
	else:
		arr = [start, stop-start]
		for i in range(items.length):
			arr.push( items[i] )
		this.splice.apply(this, arr )

@bind(Array.prototype.append)
def __array_append(item):
	this.push( item )
	#this.length += 1
	#this[this.length-1]=item
	return this

@bind(Array.prototype.__mul__)
def __array_mul(n):
	a = []
	for i in range(n):
		a.extend(this)
	return a


@bind(Array.prototype.__add__)
def __array_add(other):
	a = []
	a.extend(this)
	a.extend(other)
	return a
## helper extra `add` method for Arrays
Array.prototype.add = Array.prototype.__add__

@bind(Array.prototype.extend)
def __array_extend(other):
	#for obj in other: this.push(obj)  ## invalid because of for-in loops double reverse iter
	for i in range(other.length):
		this.push(other[i])
	return this


## nodejs 0.10.25 can not print arrays on the console if `pop` is changed?
## bad idea to change the pop of array because JIT's will probably optimze for native.
#@bind(Array.prototype.pop)
#def __array_pop(index):
#	if index is undefined:
#		return inline('this.pop()')
#	#elif index is 0:
#	#	return this.shift()
#	else:
#		return inline('this.pop()')


@bind(Array.prototype.remove)
def __array_remove(item):
	index = this.indexOf( item )
	this.splice(index, 1)

@bind(Array.prototype.insert)
def __array_insert(index, obj):
	if index < 0: index = this.length + index
	if index == 0:
		this.unshift(obj)
	else:
		this.splice(index, 0, obj)

Array.prototype.index = lambda obj : this.indexOf(obj)

@bind(Array.prototype.count)
def __array_count(obj):
	a = 0
	for item in this:
		if item is obj:  ## note that `==` will not work here, `===` is required for objects
			a += 1
	return a


## note Arrays in javascript by default sort by string order, even if the elements are numbers.
def __sort_method(ob):
	if instanceof(ob, Array):
		if ob.length and typeof(ob[0])=='number':
			def f(a,b):
				if a < b:
					return -1
				elif a > b:
					return 1
				else:
					return 0
			inline("ob.sort( f )")
		else:
			inline("ob.sort()")
	else:
		return inline("ob.sort()")


@unicode('𝑪𝒐𝒏𝒕𝒂𝒊𝒏𝒔')
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

@unicode('𝑰𝒔𝑨𝒓𝒓𝒂𝒚')
def __is_some_array( ob ):
	if __dom_array_types__.length > 0:
		for t in __dom_array_types__:
			if instanceof(ob, t):
				return True
	if ob.length is not undefined and typeof(ob.length)=='number':
		return True
	return False

@unicode('𝑰𝒔𝑻𝒚𝒑𝒆𝒅𝑨𝒓𝒓𝒂𝒚')
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




def __jsdict_get(ob, key, default_value):
	if ob.__class__ == dict:
		v = inline('ob[key]')
		if default_value is undefined and v is undefined:
			print 'KeyError: key not found in object:'
			print ob
			raise KeyError('invalid key:' + key)
		elif v is not undefined:
			return v
		else:
			return default_value

	elif typeof(ob.get)=='function':
		return inline('ob.get(key,default_value)')

	else:  ## object from an external js library.
		v = inline('ob.get(key,default_value)')
		if default_value is undefined and v is undefined:
			print 'KeyError: key not found in object:'
			print ob
			raise KeyError('invalid key:' + key)
		elif v is not undefined:
			return v
		else:
			return default_value


def __jsdict_set(ob, key, value):
	if ob.__class__ == dict:
		inline('ob[key]=value')
	elif typeof(ob.set)=='function':
		return inline('ob.set(key,value)')
	else:
		print '[method error] missing `set`'
		print ob
		raise RuntimeError('object has no method named `set`')



@unicode('𝑫𝒊𝒄𝒕_items')
def __jsdict_items(ob):
	if ob.__class__ == dict:
		items = []
		for key in ob.keys():
			items.push( [key,ob[key]] )
		return items
	elif typeof(ob.items)=='function':
		return inline('ob.items()')
	else:
		print '[method error] missing `items`'
		print ob
		raise RuntimeError('object has no method named `items`')

@unicode('𝑫𝒊𝒄𝒕_values')
def __jsdict_values(ob):
	if ob.__class__ == dict:
		items = []
		for key in ob.keys():
			items.push( ob[key] )
		return items
	elif typeof(ob.values)=='function':
		return inline('ob.values()')
	else:
		print '[method error] missing `values`'
		print ob
		raise RuntimeError('object has no method named `values`')


@unicode('𝑫𝒊𝒄𝒕_pop')
def __jsdict_pop(ob, key, __default__):
	if instanceof(ob, Array):
		if ob.length:
			## note: javascript array.pop only pops the end of an array
			## Array.splice changes the array inplace.
			if key is undefined:
				#return inline("ob.pop()")
				raise RuntimeError('Array.pop(undefined)')
			else:
				popped = ob.splice( key, 1 )
				if popped.length == 0:
					if __default__ is not undefined:  ## extra syntax: list.pop(item, default)
						return __default__
					else:
						raise IndexError(key)
				else:
					return popped[0]
		else:
			raise IndexError(key)
	elif ob.__class__ == dict:
		p = ob[key]
		if p is undefined:
			if __default__ is not undefined:
				return __default__
			else:
				raise KeyError(key)
		else:
			inline('delete ob[key]')
			return p

	elif typeof(ob.pop)=='function':
		return inline('ob.pop(key,__default__)')
	else:
		print '[method error] missing `pop`'
		print ob
		raise RuntimeError('object has no method named `items`')


def __jsdict_update(ob, other):
	if ob.__class__ == dict:
		keys = []  ## extra syntax: `for newkey in mydict.update(otherdict):`
		for key in other.keys():
			ob[key] = other[key]
			keys.push(key)
		return keys
	elif typeof(ob.update)=='function':
		return inline('ob.update(other)')
	else:
		print '[method error] missing `update`'
		print ob
		raise RuntimeError('object has no method named `update`')

@unicode('𝑺𝒆𝒕')
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
@bind(Array.prototype.bisect)
def __array_bisect(x, low, high):
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
@bind(Array.prototype.difference)
def __array_difference(other):
	f = lambda i: other.indexOf(i)==-1
	return this.filter( f )

## `&` operator
@bind(Array.prototype.intersection)
def __array_intersection(other):
	f = lambda i: other.indexOf(i)!=-1
	return this.filter( f )


## `<=` operator
@bind(Array.prototype.issubset)
def __array_issubset(other):
	for item in this:
		if other.indexOf(item) == -1:
			return False
	return True


@unicode('𝑰𝒏𝒕𝒆𝒈𝒆𝒓')
def int(a):
	a = Math.round(a)
	if isNaN(a):
		raise ValueError('not a number')
	return a


@unicode('𝑭𝒍𝒐𝒂𝒕')
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


def round(a, places):
	if places is undefined:
		places = 0
	b = '' + a
	if b.indexOf('.') == -1:
		return a
	else:
		## this could return NaN with large numbers and large places,
		## TODO check for NaN and instead fallback to `a.toFixed(places)`
		p = Math.pow(10, places)
		return Math.round(a * p) / p

@unicode('𝑺𝒕𝒓𝒊𝒏𝒈')
def str(s):
	return ''+s

## this is for compatablity with the other typed backends that use `string` instead of `str`
## it makes more sense for the user to write: `isinstance(s, string)`
def string(s):
	return ''+s

@bind(String.prototype.format)
def __string_format(fmt):
	r = this
	keys = Object.keys(fmt)
	for key in keys:
		r = r.split(key).join(fmt[key])
	r = r.split('{').join('').split('}').join('')
	return r


String.prototype.find = lambda a : this.indexOf(a)

@bind(String.prototype.isdigit)
def __string_isdigit():
	if isNaN(this):
		return False
	elif this.indexOf('.')==-1:
		return True
	else:
		return False

@bind(String.prototype.isnumber)
def __string_isnumber():
	return not isNaN(this)

#@bind(String.prototype.reverse)
#def __string_invalid_method():
#	pass


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

@unicode('𝑮𝒆𝒕𝑨𝒕𝒕𝒓𝒊𝒃𝒖𝒕𝒆')
def getattr(ob, attr):
	return __getfast__(ob, attr)

@unicode('𝑺𝒆𝒕𝑨𝒕𝒕𝒓𝒊𝒃𝒖𝒕𝒆')
def setattr(ob, attr, value):
	ob[attr] = value


def range(num, stop, step):
	"""Emulates Python's range function"""
	if stop is not undefined:
		i = num
		num = stop
	else:
		i = 0
	if step is undefined:
		step = 1
	arr = []
	while i < num:
		arr.push(i)
		i += step
	return arr

def xrange(num, stop, step):
	return range(num, stop, step)

@unicode('𝑳𝒊𝒔𝒕𝑺𝒖𝒎')   ## in math its sigma ∑
def sum( arr ):
	a = 0
	for b in arr:
		inline('a += b')
	return a

@unicode('𝑳𝒊𝒔𝒕𝑴𝒂𝒑')
def map(func, objs):
	arr = []
	for ob in objs:
		v = func(ob)
		arr.push( v )
	return arr

@unicode('𝑳𝒊𝒔𝒕𝑭𝒊𝒍𝒕𝒆𝒓')
def filter(func, objs):
	arr = []
	for ob in objs:
		if func( ob ):
			arr.push( ob )
	return arr

@unicode('𝑳𝒊𝒔𝒕𝑴𝒊𝒏')
def min( lst ):
	a = None
	for value in lst:
		if a is None: a = value
		elif value < a: a = value
	return a

@unicode('𝑳𝒊𝒔𝒕𝑴𝒂𝒙')
def max( lst ):
	a = None
	for value in lst:
		if a is None: a = value
		elif value > a: a = value
	return a

@unicode('𝑨𝒃𝒔𝒐𝒍𝒖𝒕𝒆')
def abs( num ):
	return Math.abs(num)

@unicode('𝑶𝒓𝒅𝒊𝒏𝒂𝒍')
def ord( char ):
	return char.charCodeAt(0)

@unicode('𝑪𝒉𝒂𝒓𝒂𝒄𝒕𝒆𝒓')
def chr( num ):
	return String.fromCharCode(num)


