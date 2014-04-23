'''
__getattr__, @property, and class attributes
'''
class A:
	X = 'A'

	def __getattr__(self, name):
		if name == 'hello':
			return 100
		elif name == 'world':
			return 200
		else:
			return 300

class B(A):
	Y = 'B'

	@property
	def y(self):
		return self._y

class C( B ):
	Z = 'C'

	def __init__(self, x,y,z):
		self.x = x
		self._y = y
		self._z = z

	@property
	def z(self):
		return self._z



def main():
	a = C(1,2,3)
	TestError( a.X == 'A' )
	TestError( a.Y == 'B' )
	TestError( a.Z == 'C' )

	TestError( a.x == 1 )
	TestError( a.y == 2 )
	TestError( a.z == 3 )

	b = a.hello
	TestError( b == 100 )
	TestError( a.world == 200 )
	TestError( a.XXX == 300 )
