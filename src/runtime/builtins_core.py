
inline('IndexError = function(msg) {this.message = msg || "";}; IndexError.prototype = Object.create(Error.prototype); IndexError.prototype.name = "IndexError";')
inline('KeyError   = function(msg) {this.message = msg || "";}; KeyError.prototype = Object.create(Error.prototype); KeyError.prototype.name = "KeyError";')
inline('ValueError = function(msg) {this.message = msg || "";}; ValueError.prototype = Object.create(Error.prototype); ValueError.prototype.name = "ValueError";')
inline('AttributeError = function(msg) {this.message = msg || "";}; AttributeError.prototype = Object.create(Error.prototype);AttributeError.prototype.name = "AttributeError";')
inline('RuntimeError   = function(msg) {this.message = msg || "";}; RuntimeError.prototype = Object.create(Error.prototype);RuntimeError.prototype.name = "RuntimeError";')
inline('WebWorkerError = function(msg) {this.message = msg || "";}; WebWorkerError.prototype = Object.create(Error.prototype);WebWorkerError.prototype.name = "WebWorkerError";')
inline('TypeError = function(msg) {this.message = msg || "";}; TypeError.prototype = Object.create(Error.prototype);TypeError.prototype.name = "TypeError";')

def __redef_function(src):
	this.__recompile = src
Function.prototype.redefine = __redef_function



def __debugger_overlay():
	overlay = document.getElementById('DEBUG_OVERLAY')
	if overlay is None:
		overlay = document.createElement('div')
		overlay.setAttribute('id', 'DEBUG_OVERLAY')
		document.body.appendChild(overlay)
		overlay.style.position='absolute'
		overlay.style.zIndex = 100
		overlay.style.bottom = 0
		overlay.style.right = 0
		overlay.style.width = '100%'
		overlay.style.height = '100%'
		overlay.style.backgroundColor = 'black'
		overlay.style.color = 'grey'

		header = document.createElement('h2')
		header.appendChild(document.createTextNode('header...'))
		overlay.appendChild(header)

		def _set_header(txt):
			header.firstChild.nodeValue=txt

		overlay._set_header = _set_header

		closebut = document.createElement('button')
		closebut.appendChild(document.createTextNode('close'))
		overlay.appendChild( closebut )
		closebut.style.position='absolute'
		closebut.style.bottom = 4
		closebut.style.right = 4
		def closecb(): overlay.style.visibility='hidden'
		closebut.onclick = closecb

		mbut = document.createElement('button')
		mbut.appendChild(document.createTextNode('-'))
		overlay.appendChild( mbut )
		mbut.style.position='absolute'
		mbut.style.bottom = 4
		mbut.style.right = 55
		def mbutcb():
			overlay.style.height='80%'
			overlay.style.width='70%'
		mbut.onclick = mbutcb


		subheader = document.createElement('h4')
		subheader.appendChild(document.createTextNode('subheader'))
		overlay.appendChild(subheader)

		def _set_subheader(txt):
			subheader.firstChild.nodeValue=txt

		overlay._set_subheader = _set_subheader

		cbut = document.createElement('button')
		cbut.appendChild( document.createTextNode('call') )
		cbut.style.position = 'absolute'
		cbut.style.right = 100
		header.appendChild( cbut )

		input = document.createElement('input')
		input.setAttribute('type', 'text')
		input.size = 10
		input.style.position = 'absolute'
		input.style.right = 10
		header.appendChild( input )

		overlay._header1_controls = {'call':cbut, 'args':input}


		#####################################
		ediv1 = document.createElement('div')
		ediv1.setAttribute('id', 'EDITOR1')
		overlay.appendChild(ediv1)

		header2 = document.createElement('h2')
		header2.appendChild(document.createTextNode('header2'))
		overlay.appendChild(header2)

		cbut = document.createElement('button')
		cbut.appendChild( document.createTextNode('call') )
		cbut.style.position = 'absolute'
		cbut.style.right = 100
		header2.appendChild( cbut )

		input = document.createElement('input')
		input.setAttribute('type', 'text')
		input.size = 10
		input.style.position = 'absolute'
		input.style.right = 10
		header2.appendChild( input )

		overlay._header2_controls = {'call':cbut, 'args':input}

		def _set_header2(txt):
			header2.firstChild.nodeValue=txt

		overlay._set_header2 = _set_header2


		ediv2 = document.createElement('div')
		ediv2.setAttribute('id', 'EDITOR2')
		overlay.appendChild(ediv2)
		ediv2.style.fontSize='18px'

		def __redef_on_edit(e,t):
			if t.__editfunc is not None:
				t.__editfunc.redefine( t.getValue() )

		if ace is not undefined:
			overlay.style.opacity = 0.9

			editor = ace.edit('EDITOR1')
			editor.__function = None
			editor.on('input', __redef_on_edit)
			editor.setTheme("ace/theme/monokai")
			editor.getSession().setMode("ace/mode/javascript")
			editor.renderer.setOption('showLineNumbers', false)
			editor.setOption("maxLines", 100)
			editor.setOption("minLines", 2)

			editor2 = ace.edit('EDITOR2')
			editor2.__function = None
			editor2.on('input', __redef_on_edit)

			editor2.setTheme("ace/theme/monokai")
			editor2.getSession().setMode("ace/mode/javascript")
			editor2.renderer.setOption('showLineNumbers', false)
			editor2.setAutoScrollEditorIntoView(true)
			editor2.setOption("maxLines", 100)
			editor2.setOption("minLines", 2)

		else:
			editor = document.createElement('textarea')
			editor2 = document.createElement('textarea')
			ediv1.appendChild(editor)
			ediv2.appendChild(editor2)

			editor.rows = 12
			editor.cols = 70

			editor2.rows = 12
			editor2.cols = 70

			editor.container = ediv1
			editor2.container = ediv2

			editor.appendChild(document.createTextNode(''))
			editor2.appendChild(document.createTextNode(''))

			def __getValue():
				return this.firstChild.nodeValue
			def __setValue(txt):
				this.firstChild.nodeValue = txt

			editor.getValue = __getValue
			editor.setValue = __setValue
			editor2.getValue = __getValue
			editor2.setValue = __setValue

			def __pass(): pass
			__selection = {
				'moveTo' : __pass,
				'selectWord' : __pass,
				'clearSelection' : __pass
			}
			editor.selection = __selection
			editor2.selection = __selection

	overlay.editor1 = editor
	overlay.editor2 = editor2
	return overlay


def __debugger_onerror_overlay(err,f,c):
	debugger.log(err,f,c)
	overlay = __debugger_overlay()
	editor = overlay.editor1
	editor2 = overlay.editor2

	errtype, errmsg = err.stack.splitlines()[0].split(':')
	errmsg = errmsg.strip()
	errvar = errmsg.split()[0]

	search = []
	#if errtype == 'ReferenceError':
	search.append( errvar + '.' )  ## checks for attributes
	search.append( errvar + '(' )  ## checks for func calls
	search.append( errvar + '[' )  ## checks for func calls

	errmsg_custom = []
	for i,word in enumerate(errmsg.split()):
		if i==0:
			errmsg_custom.append('`' + word + '`')
		else:
			errmsg_custom.append(word)

	search.append(errvar)

	for line in err.stack.splitlines():
		show( line.split('(')[0] )

	src1 = debugger.getsource(f)
	editor.__editfunc = None
	editor.setValue(src1)
	editor.__editfunc = f

	def callfunc1():
		f.redefine(editor.getValue())
		args = overlay._header1_controls['args'].value.split(',')
		try: f.apply(None, args)
		except:
			print 'ERROR in edited function: '+f.name
			#debugger.onerror(__exception__, f,c)

	overlay._header1_controls['call'].onclick = callfunc1

	if c is not undefined:
		overlay._set_header( errtype + ' caused in call to: `' + c.name + '`')

		def callfunc2():
			c.redefine(editor2.getValue())
			args = overlay._header2_controls['args'].value.split(',')
			try: c.apply(None, args)
			except:
				print 'ERROR in edited function: '+c.name
				#debugger.onerror(__exception__, f,c)
				#raise __exception__

		overlay._header2_controls['call'].onclick = callfunc2

		src2 = debugger.getsource(c)
		editor2.__editfunc = None
		editor2.setValue(src2)
		editor2.__editfunc = c

		foundit = False
		for i,ln in enumerate(src2.splitlines()):
			for term in search:
				if term in ln:
					editor2.selection.moveTo(i,ln.index(term))
					editor2.selection.selectWord()
					if term.endswith('('):
						errmsg_custom.insert(0, 'the function')
					else:
						errmsg_custom.insert(0, 'the variable')
					errmsg = ' '.join(errmsg_custom)
					foundit = True
					break
			if foundit:
				break

		if foundit:
			overlay._set_header2( errmsg )
		else:
			overlay._set_header2( 'function: '+c.name )
			editor2.selection.clearSelection()

		for i,ln in enumerate(src1.splitlines()):
			if not foundit:
				for term in search:
					if term in ln:
						editor.selection.moveTo(i,ln.index(term))
						editor.selection.selectWord()
						if term.endswith('('):
							errmsg_custom.insert(0, 'the function')
						else:
							errmsg_custom.insert(0, 'the variable')
						errmsg = ' '.join(errmsg_custom)
						foundit = True
						break
				if foundit:
					break
			else:
				if c.name+'(' in ln:
					editor.selection.moveTo(i,ln.index(c.name))
					editor.selection.selectWord()
					break

		if foundit:
			editor.container.style.fontSize='18px'
			editor2.container.style.fontSize='12px'
			overlay._set_header( errmsg )
			overlay._set_subheader( errtype + ' caused in call to: `' + c.name + '`')

		if src1.splitlines().length > 15:
			editor.container.style.fontSize='14px'

	## returns True uses injected breakpoints
	if __debugger__.breakpoints:
		return True
	else:
		return False


def __debugger_clean_source(f):
	source = []
	for line in f.toString().splitlines():
		if line.strip().startswith('/***/'):  ## skip injected try/catch for debugger
			continue
		else:
			source.append(line)
	return '\n'.join(source)

def __debugger_log(e,f, called):
	console.error('ABORT function->' + f.name)
	#console.warn(f.toString())
	print __debugger__.getsource( f )

	badline = None
	for line in e.stack.splitlines():
		if line.strip().startswith('at '):
			fname = line.split('(')[0][6:].strip()
			console.warn('  error in function->' + fname)
			if badline is None:
				badline = fname
			if fname == f.name:
				break
		else:
			console.error(line)

	if called is not undefined:
		console.error('exception in function->'+called.name)
		print __debugger__.getsource(called)

	return True  ## if returns True then halt (breakpoint)


__debugger__ = {
	'log'     : __debugger_log,
	'onerror' : __debugger_onerror_overlay,  ## by default do not use breakpoints
	'getsource' : __debugger_clean_source,
	'showdevtools' : lambda : require('nw.gui').Window.get().showDevTools(),
	'breakpoints'  : False,
}

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

def list(ob):
	a = []
	if ob is not undefined:
		for e in ob:
			a.push(e)
	return a

def isinstance( ob, klass):
	if ob is undefined or ob is null:
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
	elif hasattr(ob, '__class__'):
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


def issubclass(C, B):
	if C is B:
		return True
	else:
		for base in C.__bases__:
			if issubclass(base, B):
				return True
	return False

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

String.prototype.__len__ = lambda : this.length

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

def func(arr):
	out = ''
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
	isdigits = 0
	inline('for (var key in ob) { arr.push(key); if (key.isdigit()) {isdigits += 1;} }')
	if isdigits == arr.length:
		iarr = []
		for key in arr:
			iarr.push( int(key) )
		return iarr
	else:
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
def string(s):
	return ''+s

def func(fmt):
	r = this
	keys = Object.keys(fmt)
	for key in keys:
		r = r.split(key).join(fmt[key])
	r = r.split('{').join('').split('}').join('')
	return r
String.prototype.format = func


String.prototype.find = lambda a : this.indexOf(a)

def func():
	digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	for char in this:
		if char in digits: pass
		else: return False
	return True
String.prototype.isdigit = func

def func():
	digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
	for char in this:
		if char in digits: pass
		else: return False
	return True
String.prototype.isnumber = func

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

def sum( arr ):
	a = 0
	for b in arr:
		inline('a += b')
	return a

def map(func, objs):
	arr = []
	for ob in objs:
		v = func(ob)
		arr.push( v )
	return arr

def filter(func, objs):
	arr = []
	for ob in objs:
		if func( ob ):
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
	return Math.abs(num)

def ord( char ):
	char.charCodeAt(0)

def chr( num ):
	return String.fromCharCode(num)


class __WorkerPool__:
	def create_webworker(self):
		## this is lazy because if the blob is created when the js is first executed,
		## then it will pick all functions of `window` but they will be `undefined`
		## if their definition comes after the construction of this singleton.
		print 'creating blob'

		## TODO other builtins prototype hacks. see above.
		header = [
			'setInterval(',
			'	function(){',
			'		self.postMessage({time_update:(new Date()).getTime()});',
			'	}, 500',
			')',
			'Array.prototype.append = function(a) {this.push(a);};',
		]
		for name in dir(window):
			ob = window[name]
			if ob is undefined:
				print 'WARNING: object in toplevel namespace window is undefined ->' + name
			elif typeof(ob) == 'function':
				header.append( 'var ' + name + '=' + ob.toString() + ';\n' )
				for subname in dir(ob.prototype):
					sob = ob.prototype[subname]
					header.append(name + '.prototype.' +subname + '=' + sob.toString() + ';\n' )
			#elif typeof(ob) == 'object':
			#	header.append( 'var ' + name + '=' + ob.toString() + ';\n' )

		xlibs = []
		for name in self.extras:
			if '.' in name:
				print 'import webworker submodule: ' + name
				mod = name.split('.')[0]
				xname = name.split('.')[1]
				ob = eval(name)
				if typeof(ob) == 'object':  ## copy objects with static methods
					print 'import object: ' + xname
					header.append( name + '= {' )
					for sname in Object.keys(ob):
						subob = ob[sname]
						ok = True
						try:
							tmp = eval("("+subob+")")
						except:
							ok = False
						if ok:
							print 'import->: ' + sname
							header.append( '"'+sname + '":(' + ob[sname] +')' )
							header.append(',\n')
					header.pop()
					header.append('};\n')

				#if mod not in xlibs:
				#	print 'new module: '+mod
				#	header.append('var ' + mod + '= {};' )
				#	xlibs.append(mod)
			else:
				print 'import webworker module: ' + name
				header.append( 'var ' + name + '= {};\n' )
				modulemain = window[name]

				for xname in dir(modulemain):
					ob = modulemain[xname]
					if typeof(ob) == 'function':
						print 'import class: ' + xname
						header.append( name + '.' + xname + '=' + ob.toString() + ';\n' )
						if ob.prototype: ## copy methods
							#for method_name in dir(ob.prototype):
							for method_name in Object.keys(ob.prototype):
								if method_name == 'constructor': continue
								ok = True
								try:
									## getting some properties can throw deprecation errors
									sub = ob.prototype[method_name]
								except:
									ok = False

								if ok and typeof(sub) == 'function':
									print 'import method: ' + method_name
									header.append(name + '.' + xname + '.prototype.' + method_name + '=' + sub.toString() + ';' )
									#header.append(name + '.' + xname + '.' + method_name + '=' + ob.toString() + ';' )

		## Web Worker ##
		header.extend( self.source )
		blob = new(Blob(header, type='application/javascript'))
		url = URL.createObjectURL(blob)
		ww = new(Worker(url))
		#self.thread = ww  ## temp, TODO multiple threads
		#self.thread.onmessage = self.update.bind(this)

		ww._last_time_update = 0
		ww._stream_callbacks = {}
		ww._stream_triggers  = {}
		ww._get_callback  = None
		ww._call_callback = None
		ww._callmeth_callback = None

		## if worker has not sent a time update in awhile ##
		ww.busy = lambda : ww._last_time_update - time() < 1000


		def onmessage_update(evt):
			if evt.data.time_update:  ## the worker uses setInterval to report the time, see `worker.busy()`
				ww._last_time_update = evt.data.time_update
			elif evt.data.debug:
				print evt.data.debug
			else:
				ww._last_time_update = time()

				msg = evt.data.message
				if evt.data.proto: msg.__proto__ = eval(evt.data.proto + '.prototype')


				if evt.data.GET:
					ww._get_callback( msg )
				elif evt.data.CALL:
					ww._call_callback( msg )
				elif evt.data.CALLMETH:
					ww._callmeth_callback( msg )
				else:
					id = evt.data.id
					if id in ww._stream_callbacks:  ## channels
						callbacks = ww._stream_callbacks[id]
						if len(callbacks):
							cb = callbacks.pop()
							cb( msg )
						else:
							ww._stream_triggers[id].push( msg )
					else:
						print 'ERROR: missing callback for:' + id


		ww.onmessage = onmessage_update
		return ww

	def __init__(self, src, extras):
		## note:  src is an array
		## note: thread-ids = `cpu-id:spawned-id`
		self.source = src
		self.extras = extras
		self.thread = None
		self.workers = {}
		self.pending = {}
		self._get  = None
		self._call = None
		self._callmeth = None

	def update(self, evt):
		if evt.data.debug:
			print evt.data.debug
		else:
			id = evt.data.id
			msg = evt.data.message
			if evt.data.proto: msg.__proto__ = eval(evt.data.proto + '.prototype')


			if evt.data.GET:
				self._get( msg )
				#self._get = None
			elif evt.data.CALL:
				self._call( msg )
				#self._call = None
			elif evt.data.CALLMETH:
				self._callmeth( msg )
				#self._callmeth = None

			elif id in self.workers:  ## channels
				callbacks = self.workers[id]
				if len(callbacks):
					cb = callbacks.pop()
					cb( msg )
				else:
					self.pending[id].push( msg )
			else:
				print 'ERROR: missing callback for:' + id

	def spawn(self, cfg, options):
		cpu = '0'
		if options is not undefined:
			print options.cpu
			cpu = options.cpu

		#if tid not in self.threads:
		#	self.threads[tid] = self.create_webworker()
		#cfg['thread-id'] = tid
		#return tid + '|' + self.threads[tid].spawn_class(cfg)

		readythread = None
		for thread in self.pool:
			if not thread.busy():
				readythread = thread
				break

		if not readythread:
			self.pool.append(
				self.create_webworker()
			)

		## cfg contains: call|new:func/classname, args:[]
		id = 'worker' + len(self.workers)
		self.workers[id] = []  ## callbacks
		self.pending[id] = []  ## early messages
		cfg['spawn'] = id
		self.thread.postMessage(cfg)
		return id

	def send(self, id=None, message=None):
		#tid, sid = id.split('|')
		#if tid not in self.threads:
		#	raise RuntimeError('invalid thread-webworker id')

		try:
			self.thread.postMessage({'send':id, 'message':message})
			#self.threads[tid].postMessage({'send':id, 'message':message})

		except:
			print 'DataCloneError: can not send data to webworker'
			print message
			raise RuntimeError('DataCloneError: can not send data to webworker')

	def recv(self, id, callback):
		if id in self.pending and self.pending[id].length:
			res = self.pending[id].pop()
			callback(res)
		elif id in self.workers:
			self.workers[id].insert(0, callback)
		else:
			if id is undefined:
				raise WebWorkerError("undefined id")
			else:
				raise WebWorkerError(id)

	def get(self, id, attr, callback):
		self._get = callback
		self.thread.postMessage({'id':id, 'get':attr})

	def call(self, func, args, callback):
		self._call = callback
		self.thread.postMessage({'call':func, 'args':args})


	def callmeth(self, id, func, args, callback):
		self._callmeth = callback
		self.thread.postMessage({'id':id, 'callmeth':func, 'args':args})
