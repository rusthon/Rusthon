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

main()
