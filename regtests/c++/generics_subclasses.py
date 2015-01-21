'''
generics classes with common base.
'''
class A:
	def __init__(self, x:int):
		self.x = x

	def method1(self) -> int:
		return self.x

class B(A):

	def method1(self) ->int:
		return self.x * 2

class C(A):

	def method1(self) ->int:
		return self.x + 200

class D:
	def __init__(self, x:int):
		self.x = x

	def method1(self) -> int:
		return self.x

## rusthon generates the same method for all subclass of `A` ##
def my_generic( g:A ) ->int:
	return g.method1()


def my_generic2( g1:A, g2:A ) ->int:
	return g1.method1() * g2.method1()

def main():
	a = A( 100 )
	b = B( 100 )
	c = C( 100 )

	x = my_generic( a )
	TestError(a.x == x )
	print(x)

	y = my_generic( b )
	TestError( y==200 )
	print(y)

	z = my_generic( c )
	TestError( z==300 )
	print(z)
	print('----------------')
	print( my_generic2(a,b))
	print( my_generic2(b,c))
