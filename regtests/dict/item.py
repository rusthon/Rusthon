from runtime import *
"""__getitem__"""

def f(): pass
class G(object):
	def get(self, x,y=None):
		if y: return y
		else: return x
	def set(self, x,y):
		print 'set method ok'
		print x, y
		return True
	def items(self):
		return True

	def pop(self, x):
		return x

def main():
	g = G()

	## mixing string and number keys in a dict literal
	## is not allowed, and will raise SyntaxError at transpile time.
	#a = {'2': 22, 3:33}

	## this dict has inferred int keys, other key types are not allowed ##
	a = {2: 22, 3:33}

	assert(a[2] == 22)
	assert(a[3] == 33)

	## these raise TypeError at runtime, because the keytypes are invalid
	#a[f] = 44
	#a[g] = 66
	#a[G] = 55
	#assert(a[f] == 44)
	#assert(a[G] == 55)
	#assert(a[g] == 66)

	print a.get(1, 'getok')
	assert a.get('none', 'default') == 'default'
	assert g.get(1)==1
	assert g.get(0, y=2)==2

	a.set(0, 'hi')
	assert a[0]=='hi'

	assert g.set(1,2)
	print 'ok'

	i = a.items()
	print i
	assert len(i)==3

	assert g.items()

	v = a.values()
	print v
	assert len(v)==3

	p = a.pop(2)
	assert p==22
	assert 2 not in a.keys()

	o = a.pop('missing', 'X')
	assert o=='X'

	print a.keys()
	assert a.keys().length == 2

	assert g.pop(100)==100

	print 'testing dict.update'
	u = {1:'x', 2:'y'}
	newkeys = a.update( u )
	print newkeys
	assert 1 in a.keys()
	assert 2 in a.keys()
	assert 'x' in a.values()
	assert 'y' in a.values()

	for newkey in a.update({66:'XXX', 99:'YYY'}):
		print 'new key:' + newkey

	print 'ok'

main()
