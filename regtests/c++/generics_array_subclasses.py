'''
generics classes with common base.
'''
class A:
	def __init__(self, x:int):
		self.x = x

	def method1(self) -> int:
		return self.x
	def getname(self) -> string:
		return self.__class__

class B(A):
	def method1(self) ->int:
		return self.x * 2

class C(A):
	def method1(self) ->int:
		return self.x + 200

	def say_hi(self):
		print('hi from C')


def my_generic( g:A ) ->int:
	return g.method1()


def main():
	a = A( 1 )
	b = B( 200 )
	c = C( 3000 )

	print(a.__class__)
	print(b.__class__)
	print(c.__class__)
	print('- - - - - - -')

	arr = []A( a,b,c )
	for item in arr:
		## just prints 100's because c++ runtime method dispatcher thinks item
		## is of class type `A`
		print(item.__class__)
		print( my_generic(item) )

	print('- - - - - - -')

	for item in arr:
		print(item.getname())
		print(item.x)

		## to get to the real subclasses, we need if-isinstance
		if isinstance(item, B):
			print('is B')
			my_generic( item )
		if isinstance(item, C):
			print('is C')
			my_generic( item )
			#item.say_hi()  ## TODO

