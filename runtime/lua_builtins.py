JS("""
__NULL_OBJECT__ = {}

__get__ = function(ob, name)
	if name == '__call__' then
		return ob
	end
end

__add_op = function(a,b)
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
