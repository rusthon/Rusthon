JS("""
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

__test_if_true__ = function( x )
	if x == 0 then
		return false
	elseif x == nil then
		return false
	else
		return true
	end
end

__get__ = function(ob, name)
	if name == '__call__' then
		if type(ob)=='function' then
			return ob
		else
			return ob.__call__
		end
	elseif name == '__iter__' then
		local iter = {
			index = 1,
			length = #ob,
			object = ob,
			next_fast = function(self)
				local x = self.object[ self.index ]
				self.index = self.index + 1
				return x
			end
		}
		return iter
	else
		return ob[ name ]
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
		object = {
			__class__ = class,
			__dict__ = 'TODO'
		}
		for k,v in pairs(attrs) do
			if type(v)=='function' then
				object[ k ] = function(_args, _kwargs)
					a = {object}
					return v(__concat_tables_array(a, _args), _kwargs)
				end
			else
				object[ k ] = v
			end
		end
		a = {object}
		attrs.__init__( __concat_tables_array(a, args), kwargs )
		return object
	end
	return class
end


__add_op = function(a,b)
	if type(a) == 'string' then
		return a .. b
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
	return tostring(ob)

def int(ob):
	return tonumber(ob)

def float(ob):
	return tonumber(ob)

class list:
	'''
	Array length in Lua must be manually tracked, because a normal for loop will not
	properly loop over a sparse Array with nil holes.
	'''
	def __init__(self, items, pointer=None, length=0):
		with lowlevel:
			self.length = length
			if pointer:
				self[...] = pointer
			else:
				self[...] = {}

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
		if stop == null and step == null:
			return self[...].sublist( start )
		elif stop < 0:
			stop = self[...].length + stop
			return self[...].sublist(start, stop)

	def __add__(self, other):
		for item in other:
			self.append( item )

	def append(self, item):
		with lowlevel:
			self.length += 1
			self[...][ self.length ] = item

	def index(self, obj):
		with lowlevel:
			i = 1
			while i < self.length:
				if self[...][i] == obj:
					return i
				i += 1
