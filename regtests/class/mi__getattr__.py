from runtime import *
'''
__getattr__ and @property
'''
class Root:
	def __getattr__(self, name):
		if name == 'x':
			return self._x
		elif name == 'y':
			return self._y
		else:
			return name

class A( Root ):
	def __init__(self):
		self._x = 1
		self._y = 2

class B( A ):
	@property
	def w(self):
		return 'XXX'

def unknown(u):
	return u



def main():
	a = A()
	b = unknown( a )
	assert( b.x==1 )
	assert( b.y==2 )
	assert( b.z=='z' )
	assert( b.w=='w' )

	c = B()
	d = unknown( c )
	assert( d.x==1 )
	assert( d.y==2 )
	assert( d.z=='z' )
	assert( d.w=='XXX' )

main()
