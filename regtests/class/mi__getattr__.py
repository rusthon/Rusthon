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
	TestError( b.x==1 )
	TestError( b.y==2 )
	TestError( b.z=='z' )
	TestError( b.w=='w' )

	c = B()
	d = unknown( c )
	TestError( d.x==1 )
	TestError( d.y==2 )
	TestError( d.z=='z' )
	TestError( d.w=='XXX' )
