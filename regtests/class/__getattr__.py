from runtime import *
'''
__getattr__, @property, and class attributes
'''
class A:
	X = 'A'

	## not allowed - will raise SyntaxError at compile time ##
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
	## GOTCHA: this is not allowed in Rusthon,
	## class variables can only be used on the classes,
	## not on the instances.
	#assert( a.X == 'A' )
	#assert( a.Y == 'B' )
	#assert( a.Z == 'C' )

	assert( A.X == 'A' )
	assert( B.Y == 'B' )
	assert( C.Z == 'C' )


	assert( a.x == 1 )
	#assert( a.y == 2 )  ## TODO fix me
	assert( a.z == 3 )

	## GOTCHA: __getattr__ is not allowed in Rusthon
	#b = a.hello
	#assert( b == 100 )
	#assert( a.world == 200 )
	#assert( a.XXX == 300 )

main()
