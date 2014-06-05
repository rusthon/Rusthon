# PythonJS Low Level Runtime
# by Amirouche Boubekki and Brett Hartshorn - copyright 2013
# License: "New BSD"

__NULL_OBJECT__ = Object.create( null )
if 'window' in this and 'document' in this:
	__WEBWORKER__ = False
	__NODEJS__ = False
elif typeof(process) != 'undefined':
	## note, we can not test for '"process" in global'
	## make sure we are really inside NodeJS by letting this fail, and halting the program.
	__WEBWORKER__ = False
	__NODEJS__ = True
else:
	__NODEJS__ = False
	__WEBWORKER__ = True

#if __NODEJS__:
#	require('requirejs')

def __create_array__():  ## DEPRECATED
	"""Used to fix a bug/feature of Javascript where new Array(number)
	created a array with number of undefined elements which is not
	what we want"""
	var(i, array)
	array = []
	i = 0
	while i < arguments.length:
		array.push(arguments[i])
		i += 1
	return array


def __get__(object, attribute, error_message):
	"""Retrieve an attribute, method, property, or wrapper function.

	method are actually functions which are converted to methods by
	prepending their arguments with the current object. Properties are
	not functions!

	DOM support:
		http://stackoverflow.com/questions/14202699/document-createelement-not-working
		https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof

	Direct JavaScript Calls:
		if an external javascript function is found, and it was not a wrapper that was generated here,
		check the function for a 'cached_wrapper' attribute, if none is found then generate a new
		wrapper, cache it on the function, and return the wrapper.
	"""
	if object is None:
		if error_message:
			raise AttributeError('(`null` has no attributes) ' +error_message)
		else:
			raise AttributeError('null object (None) has no attribute: '+attribute)
	elif object is undefined:
		if error_message:
			raise AttributeError('(`undefined` has no attributes) ' +error_message)
		else:
			raise AttributeError('undefined has no attribute: ' +attribute)

	if attribute == '__call__':
		if object.pythonscript_function or object.is_wrapper:  ## common case
			return object
		elif object.cached_wrapper:  ## rare case
			return object.cached_wrapper

		elif JS("{}.toString.call(object) === '[object Function]'"):
			## TODO double check that this is not a pythonjs function
			def wrapper(args,kwargs):  ## dyanmically wrap external javascript function
				var(i, arg, keys)
				if args != None:
					i = 0
					while i < args.length:
						arg = args[i]
						#if instanceof(arg, Object): ## fails on objects created by Object.create(null)
						if arg and typeof(arg) == 'object':
							if arg.jsify:
								args[i] = arg.jsify()
						i += 1

				if kwargs != None:
					keys = __object_keys__(kwargs)
					if keys.length != 0:
						args.push( kwargs )
						i = 0
						while i < keys.length:
							arg = kwargs[ keys[i] ]
							if arg and typeof(arg) == 'object':
								if arg.jsify:
									kwargs[ keys[i] ] = arg.jsify()
							i += 1

				return object.apply(None, args)

			wrapper.is_wrapper = True
			object.cached_wrapper = wrapper
			return wrapper


	if Object.hasOwnProperty.call(object, '__getattribute__'):
		return object.__getattribute__( attribute )


	var(attr)
	attr = object[attribute]  ## this could be a javascript object with cached method


	if __NODEJS__ is False and __WEBWORKER__ is False:
		if JS("object instanceof HTMLDocument"):
			#print 'DYNAMIC wrapping HTMLDocument'
			if JS("typeof(attr) === 'function'"):
				def wrapper(args,kwargs): return attr.apply(object, args)
				wrapper.is_wrapper = True
				return wrapper
			else:
				return attr
		elif JS("object instanceof HTMLElement"):
			#print 'DYNAMIC wrapping HTMLElement'
			if JS("typeof(attr) === 'function'"):
				def wrapper(args,kwargs): return attr.apply(object, args)
				wrapper.is_wrapper = True
				return wrapper
			else:
				return attr

	## attr can be null and will return, undefined will raise AttributeError ##		
	if attr is not undefined:
		if typeof(attr) == 'function':
			if JS("attr.pythonscript_function === undefined && attr.is_wrapper === undefined"):

				## if there is a prototype with methods, then we can be sure that the user indends to call `new` on it,
				## however rare, it is still possible that it is a constructor without a prototype of any length,
				## in that case the user must call `new` and using the full scope, because things inside a `new`
				## call are not wrapped, ie: `new(A.B.C.xxx(args))`
				if instanceof(attr.prototype, Object) and Object.keys(attr.prototype).length > 0:
					return attr

				def wrapper(args,kwargs):
					#if instanceof(args, Array):
					var(i, arg, keys)
					if args != None:
						i = 0
						while i < args.length:
							arg = args[i]
							if arg and typeof(arg) == 'object':
								if arg.jsify:
									args[i] = arg.jsify()
							i += 1

					if kwargs != None:
						keys = __object_keys__(kwargs)
						if keys.length != 0:
							args.push( kwargs )
							i = 0
							while i < keys.length:
								arg = kwargs[ keys[i] ]
								if arg and typeof(arg) == 'object':
									if arg.jsify:
										kwargs[ keys[i] ] = arg.jsify()
								i += 1

					return attr.apply(object, args)
					#else:  ## TODO are there cases where this is needed?
					#	return attr.apply(object, arguments)

				wrapper.is_wrapper = True
				wrapper.wrapped = attr  ## this is required because some javascript API's `class-method-style` helper functions on the constructor
				return wrapper


			elif attr.is_classmethod:

				def method():
					var(args)
					args =  Array.prototype.slice.call(arguments)
					if (JS('args[0] instanceof Array') and JS("{}.toString.call(args[1]) === '[object Object]'") and args.length == 2):
						pass
					else:
						args = [args, JSObject()]
					if object.__class__:  ## if classmethod is called from an instance, force class as first argument
						args[0].splice(0, 0, object.__class__)
					else:
						args[0].splice(0, 0, object)
					return attr.apply(this, args)  ## this is bound so that callback methods can use `this` from the caller

				method.is_wrapper = True
				object[attribute] = method  ## cache method - we assume that class methods do not change
				return method

			else:
				return attr

		else:
			return attr

	var(__class__, bases)


	#attr = object[ attribute ]
	#if attr != None:
	#	return attr


	# next check for object.__class__
	__class__ = object.__class__
	if __class__:  ## at this point we can assume we are dealing with a pythonjs class instance

		if attribute in __class__.__properties__:  ## @property decorators - TODO support PythonJSJS classes
			return __class__.__properties__[ attribute ]['get']( [object], JSObject() )

		if attribute in __class__.__unbound_methods__:
			attr = __class__.__unbound_methods__[ attribute ]
			if attr.fastdef:
				def method(args,kwargs):
					if arguments and arguments[0]:
						arguments[0].splice(0,0,object)
						return attr.apply(this, arguments)
					else:
						return attr( [object], {} )
			else:
				def method(args,kwargs):
					if arguments.length == 0:
						return attr( [object], __NULL_OBJECT__ )
					elif instanceof(args,Array) and typeof(kwargs) is "object" and arguments.length==2:
						args.splice(0, 0, object)
						if kwargs is undefined:
							return attr( args, __NULL_OBJECT__ )
						else:
							return attr( args, kwargs )
					else:
						args = Array.prototype.slice.call(arguments)
						args.splice(0, 0, object)
						args = [args, __NULL_OBJECT__]  ## TODO - way to pass keyword args from javascript?
						return attr.apply(this, args)  ## this is bound here so that callback methods can use `this` from the caller

			method.is_wrapper = True
			object[attribute] = method  ## cache method - we assume that methods do not change
			return method


		attr = __class__[ attribute ]

		if attribute in __class__:
			if JS("{}.toString.call(attr) === '[object Function]'"):
				if attr.is_wrapper:
					return attr
				elif attr.fastdef:
					def method(args,kwargs):
						if arguments and arguments[0]:
							arguments[0].splice(0,0,object)
							return attr.apply(this, arguments)
						else:
							return attr( [object], {} )
				else:
					def method(args,kwargs):
						if arguments.length == 0:
							return attr( [object], __NULL_OBJECT__ )
						elif instanceof(args,Array) and typeof(kwargs) is "object" and arguments.length==2:
							args.splice(0, 0, object)
							if kwargs is undefined:
								return attr( args, __NULL_OBJECT__ )
							else:
								return attr( args, kwargs )
						else:
							args = Array.prototype.slice.call(arguments)
							args.splice(0, 0, object)
							args = [args, __NULL_OBJECT__]  ## TODO - way to pass keyword args from javascript?
							return attr.apply(this, args)  ## this is bound here so that callback methods can use `this` from the caller


				method.is_wrapper = True
				object[attribute] = method  ## cache method - we assume that methods do not change
				return method
			else:
				return attr

		bases = __class__.__bases__

		for base in bases:
			attr = _get_upstream_attribute(base, attribute)
			if attr is not undefined:
				if JS("{}.toString.call(attr) === '[object Function]'"):

					if attr.fastdef:
						def method(args,kwargs):
							if arguments and arguments[0]:
								arguments[0].splice(0,0,object)
								return attr.apply(this, arguments)
							else:
								return attr( [object], {} )
					else:
						def method(args,kwargs):
							if arguments.length == 0:
								return attr( [object], __NULL_OBJECT__ )
							elif instanceof(args,Array) and typeof(kwargs) is "object" and arguments.length==2:
								args.splice(0, 0, object)
								if kwargs is undefined:
									return attr( args, __NULL_OBJECT__ )
								else:
									return attr( args, kwargs )
							else:
								args = Array.prototype.slice.call(arguments)
								args.splice(0, 0, object)
								args = [args, __NULL_OBJECT__]  ## TODO - way to pass keyword args from javascript?
								return attr.apply(this, args)  ## this is bound here so that callback methods can use `this` from the caller



					method.is_wrapper = True
					object[attribute] = method  ## cache method - we assume that methods do not change
					return method
				else:
					return attr

		for base in bases:  ## upstream property getters come before __getattr__
			var( prop )
			prop = _get_upstream_property(base, attribute)
			if prop is not undefined:
				return prop['get']( [object], JSObject() )

		if '__getattr__' in __class__:
			return __class__['__getattr__']( [object, attribute], JSObject() )

		for base in bases:
			var( f )
			f = _get_upstream_attribute(base, '__getattr__')
			if f is not undefined:
				return f( [object, attribute], JSObject() )


	## getting/setting from a normal JavaScript Object ##
	if attribute == '__getitem__':
		def wrapper(args,kwargs): return object[ args[0] ]
		wrapper.is_wrapper = True
		return wrapper
	elif attribute == '__setitem__':
		def wrapper(args,kwargs): object[ args[0] ] = args[1]
		wrapper.is_wrapper = True
		return wrapper

	if typeof(object, 'function') and object.is_wrapper:
		return object.wrapped[ attribute ]

	if attribute == '__iter__' and instanceof(object, Object):
		def wrapper(args, kwargs): return new( __ArrayIterator(Object.keys( object ),0) )
		wrapper.is_wrapper = True
		return wrapper

	if attribute == '__contains__' and instanceof(object, Object):
		def wrapper(args, kwargs): return (Object.keys( object )).indexOf( args[0] ) != -1
		wrapper.is_wrapper = True
		return wrapper


	if attr is undefined:
		if error_message:
			raise AttributeError(error_message)
		else:
			raise AttributeError(attribute)
	else:
		return attr

def _get_upstream_attribute(base, attr):
	if attr in base:
		return base[ attr ]
	for parent in base.__bases__:
		return _get_upstream_attribute(parent, attr)

def _get_upstream_property(base, attr):  ## no longer required
	if attr in base.__properties__:
		return base.__properties__[ attr ]
	for parent in base.__bases__:
		return _get_upstream_property(parent, attr)

def __set__(object, attribute, value):
	'''
	__setattr__ is always called when an attribute is set,
	unlike __getattr__ that only triggers when an attribute is not found,
	this asymmetry is in fact part of the Python spec.
	note there is no __setattribute__

	In normal Python a property setter is not called before __setattr__,
	this is bad language design because the user has been more explicit
	in having the property setter.

	In PythonJS, property setters are called instead of __setattr__.
	'''

	if '__class__' in object and object.__class__.__setters__.indexOf(attribute) != -1:
		object[attribute] = value
	elif '__setattr__' in object:
		object.__setattr__( attribute, value )
	else:
		object[attribute] = value



def __getargs__(func_name, signature, args, kwargs):
	"""Based on ``signature`` and ``args``, ``kwargs`` parameters retrieve
	the actual parameters.

	This will set default keyword arguments and retrieve positional arguments
	in kwargs if their called as such"""

	if args is None: args = []
	if kwargs is None: kwargs = {}
	out = {}

	# if the caller did not specify supplemental positional arguments e.g. *args in the signature
	# raise an error
	if args.length > signature.args.length:
		if signature.vararg:
			pass
		else:
			print 'Error in function->' + func_name
			print 'args:', args, 'kwargs:', kwargs, 'sig:', signature
			raise TypeError("Supplemental positional arguments provided but signature doesn't accept them")

	j = 0
	while j < signature.args.length:
		name = signature.args[j]
		if name in kwargs:
			# value is provided as a keyword argument
			out[name] = kwargs[name]
		elif j < args.length:
			# value is positional and within the signature length
			out[name] = args[j]
		elif name in signature.kwargs:
			# value is not found before and is in signature.length
			out[name] = signature.kwargs[name]
		j += 1

	args = args.slice(j)  ## note that if this fails because args is not an array, then a pythonjs function was called from javascript in a bad way.
	#args = Array.prototype.slice.call(args, j)  ## this fix should not be required

	if signature.vararg:
		out[signature.vararg] = args
	if signature.varkwarg:
		out[signature.varkwarg] = kwargs
	return out

