JS("""

local __bitops__ = require('bit')
__NULL_OBJECT__ = {}

__concat_tables_array = function(t1, t2)
	for i=1,#t2 do
		t1[ #t1+1 ] = t2[i]
	end
	return t1
end

__concat_tables = function(t1, t2)
	for k,v in pairs(t2) do
		t1[k] = v
	end
	return t1
end

function table.shallow_copy(t)
	local t2 = {}
	for k,v in pairs(t) do
		t2[k] = v
	end
	return t2
end

__test_if_true__ = function( x )
	if x == true then return true
	elseif x == false then return false
	elseif x == nil then return false
	elseif x == '' then return false

	elseif type(x) == 'number' then
		if x == 0 then return false
		else return true
		end

	elseif x.__class__ and x.__class__.__name__ == 'list' then
		if x.length > 0 then return true
		else return false end
	elseif x.__class__ and x.__class__.__name__ == 'dict' then
		if x.keys().length > 0 then return true
		else return false end
	else
		return true
	end
end

__set__ = function(ob, name, value)
	ob[ name ] = value
end

__get__ = function(ob, name)
	if name == '__call__' then
		if type(ob)=='function' then
			return ob
		else
			return ob.__call__
		end
	elseif type(ob)=='string' then
		return __get__helper_string(ob,name)
	elseif ob.__getters__ and ob.__getters__[name] then
		return ob.__getters__[name]( ob )  --unbound method--
	elseif ob[name]==nil and ob.__getattr__ then
		return ob.__getattr__( {name} )
	else
		return ob[ name ]
	end
end

__sprintf = function(s, args)
	if type(args)=='table' then
		return string.format(s, unpack(args))
	else
		return string.format(s, args)
	end
end

function string:to_array()
	local i = 1
	local t = {}
	for c in self:gmatch('.') do
		t[ i ] = c
		i = i + 1
	end
	return t
end

function string:split(sSeparator, nMax, bRegexp)
	assert(sSeparator ~= '')
	assert(nMax == nil or nMax >= 1)
	if sSeparator == nil then
		sSeparator = ' '
	end

	local aRecord = {}

	if self:len() > 0 then
		local bPlain = not bRegexp
		nMax = nMax or -1

		local nField=1 nStart=1
		local nFirst,nLast = self:find(sSeparator, nStart, bPlain)
		while nFirst and nMax ~= 0 do
			aRecord[nField] = self:sub(nStart, nFirst-1)
			nField = nField+1
			nStart = nLast+1
			nFirst,nLast = self:find(sSeparator, nStart, bPlain)
			nMax = nMax-1
		end
		aRecord[nField] = self:sub(nStart)
	end
	return aRecord
end

__bind_methods__ = function(object, class)
	for k,v in pairs( class.__attributes__ ) do
		if object[k] == nil then
			if type(v)=='function' then
				object[ k ] = function(_args, _kwargs)
					local o = {object}
					if _args then
						return v(__concat_tables_array(o, _args), _kwargs or {})
					else
						return v(o, _kwargs or {})
					end
				end
			else
				-- TODO class attribute should have dynamic look up.
				object[ k ] = v
			end
		end
	end
	for k,v in pairs( class.__bases__ ) do
		__bind_methods__( object, v )
	end
end

__bind_properties__ = function(object, class)
	for k,v in pairs( class.__properties__ ) do
		assert( type(v.get)=='function' )
		if object.__getters__[k] == nil then
			object.__getters__[k] = v.get   --unbound method--
		end
	end
	for k,v in pairs( class.__bases__ ) do
		__bind_properties__( object, v )
	end
end


__create_class__ = function(class_name, parents, attrs, props)
	local class = {
		__bases__ = parents,
		__name__ = class_name,
		__properties__ = props,
		__attributes__ = attrs
	}
	function class.__call__( args, kwargs )
		local object = {
			__class__ = class,
			__dict__ = 'TODO',
			__getters__ = {}
		}
		__bind_methods__( object, class )
		__bind_properties__( object, class )

		for k,v in pairs( class.__attributes__ ) do
			class[ k ] = v
		end

		if object.__init__ then
			object.__init__( args, kwargs )
		end
		return object
	end
	return class
end


__add_op = function(a,b)
	if type(a) == 'string' then
		return a .. b
	elseif type(a) == 'table' and a.__class__ then
		return a.__add__({b}, {})
	else
		return a + b
	end
end

__add__ = function(a,b)
	if type(a) == 'string' then
		return a .. b
	else
		return a + b
	end
end

""")

def str(ob):
	with lowlevel:
		return tostring(ob)

def int(ob):
	with lowlevel:
		return tonumber(ob)

def float(ob):
	with lowlevel:
		return tonumber(ob)

def len(ob):
	with lowlevel:
		if type(ob) == 'string':
			return string.len(ob)
		else:
			return ob.length

def chr(a):
	with lowlevel:
		return string.char(a)

def ord(a):
	with lowlevel:
		return string.byte(a)

def getattr(ob, name):
	with lowlevel:
		return ob[name]  ## could be None (nil), no good way to raise AttributeError

def isinstance( ob, klass ):
	if ob == None:
		return False
	elif ob.__class__:
		if ob.__class__.__name__ == klass.__name__:
			return True
		else:
			return False
	else:
		return False

def sum( arr ):
	a = 0
	for b in arr:
		a += b
	return a

class __iterator_string:
	def __init__(self, obj, index):
		with lowlevel:
			self.obj = obj
			self.index = index
			self.length = string.len(obj)

	def next(self):
		with lowlevel:
			index = self.index
			self.index += 1
			return string.sub( self.obj, index+1, index+1 )

class __iterator_list:
	def __init__(self, obj, index):
		self.obj = obj
		self.index = index
		self.length = len(obj)

	def next(self):
		with lowlevel:
			index = self.index
			self.index += 1
			return self.obj[...][index+1]


class list:
	'''
	Array length in Lua must be manually tracked, because a normal for loop will not
	properly loop over a sparse Array with nil holes.
	'''
	def __init__(self, items, pointer=None, length=0):
		with lowlevel:
			self.length = length
			if type(items)=='string':
				self[...] = string.to_array( items )
				self.length = string.len(items)
			elif type(items)=='table' and items.__class__ and items.__class__.__name__=='list':
				print('HIT TABLE!!!')
			elif pointer:
				self[...] = pointer
			else:
				self[...] = {}

	def __contains__(self, value):
		with lowlevel:
			for v in self[...]:
				if v == value:
					return True
			return False

	def __getitem__(self, index):
		with lowlevel:
			if index < 0:
				index = self.length + index
			return self[...][index+1]

	def __setitem__(self, index, value):
		with lowlevel:
			if index < 0:
				index = self.length + index
			self[...][index+1] = value

	def __getslice__(self, start, stop, step):
		if stop == None and step == None:
			with lowlevel:
				copy = table.shallow_copy( self[...] )
			return list( pointer=copy, length=self.length )
		elif stop < 0:  ## TODO
			pass

	def __iter__(self):
		return __iterator_list(self, 0)

	def __add__(self, other):
		with lowlevel:
			ptr = table.shallow_copy( self[...] )
		copy = list( pointer=ptr, length=self.length )
		for item in other:
			copy.append( item )
		return copy

	def append(self, item):
		with lowlevel:
			self.length += 1
			self[...][ self.length ] = item

	def index(self, obj):
		with lowlevel:
			i = 0
			while i < self.length:
				if self[...][i+1] == obj:
					return i
				i += 1

tuple = list
## this must come after list because list.__call__ is used directly,
## and the lua compiler can not use forward references.
JS('''

__create_list = function(size)
	return __get__(list, "__call__")({}, {pointer={},length=size})
end

__get__helper_string = function(s, name)
	local wrapper
	if name == '__getitem__' then
		wrapper = function(args, kwargs)
			return string.sub(s, args[1]+1, args[1]+1)
		end

	elseif name == '__contains__' then
		wrapper = function(args, kwargs)
			if s:find( args[1] ) then return true
			else return false end
		end

	elseif name == '__getslice__' then
		wrapper = function(args, kwargs)
			if args[1]==nil and args[2]==nil and args[3]==-1 then
				return s:reverse()
			end
		end

	elseif name == '__iter__' then
		wrapper = function(args, kwargs)
			return __iterator_string.__call__( {s, 0} )
		end

	elseif name == 'upper' then
		wrapper = function(args, kwargs)
			return string.upper(s)
		end
	elseif name == 'lower' then
		wrapper = function(args, kwargs)
			return string.lower(s)
		end
	elseif name == 'split' then
		wrapper = function(args, kwargs)
			local a
			if args then
				a = s:split( args[1] )
			else
				a = s:split()
			end
			return list.__call__( {}, {pointer=a, length=#a} )
		end
	else
		print('ERROR: NotImplemented')
	end

	return wrapper
end
''')

def range(num, stop):
	"""Emulates Python's range function"""
	if stop is not None:
		i = num
		num = stop
	else:
		i = 0
	arr = []
	while i < num:
		arr.append(i)
		i += 1
	return arr

class dict:
	def __init__(self, object, pointer=None):
		with lowlevel:
			self[...] = {}
			if pointer:
				self[...] = pointer
			elif object:
				for d in object: ## array
					self[...][ d.key ] = d.value
					

	def __getitem__(self, key):
		with lowlevel:
			return self[...][ key ]

	def __setitem__(self, key, value):
		with lowlevel:
			self[...][ key ] = value

	def keys(self):
		with lowlevel:
			ptr = []
			i = 1
			for k,v in pairs(self[...]):
				ptr[ i ] = k
				i = i + 1
		return list( pointer=ptr, length=i-1 )

	def __iter__(self):
		return self.keys().__iter__()

	def items(self):
		with lowlevel:
			ptr = []
			i = 1
			for k,v in pairs(self[...]):
				p = [k,v]
				item = list.__call__([], {pointer:p, length:2})
				ptr[ i ] = item
				i = i + 1
		return list( pointer=ptr, length=i-1 )
