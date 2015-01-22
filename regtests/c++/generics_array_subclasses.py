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

def my_generic( g:A ) ->int:
	return g.method1()


def main():
	a = A( 100 )
	b = B( 100 )
	c = C( 100 )

	arr = []A( a,b,c )
	for item in arr:
		print( my_generic(item) )

