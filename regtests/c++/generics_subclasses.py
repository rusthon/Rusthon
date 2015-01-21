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

## c++ allows this type of Generics ##
def my_generic( g:A ) ->int:
	return g.method1()
def my_generic( g:B ) ->int:
	return g.method1()
def my_generic( g:C ) ->int:
	return g.method1()

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