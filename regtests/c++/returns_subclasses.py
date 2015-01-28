'''
returns subclasses
'''
class A:
	def __init__(self, x:int):
		self.x = x

	def method(self) -> int:
		return self.x

	def foo(self) ->int:
		return self.x * 2
	def bar(self) ->int:
		return self.x + 200


class B(A):

	def foo(self) ->int:
		return self.x * 2

class C(A):

	def bar(self) ->int:
		return self.x + 200


def some_subclass( x:int ) ->A:
	switch x:
		case 0:
			a = A(1)
			return a
		case 1:
			b = B(2)
			return b as A
		case 3:
			c = C(3)
			return c as A


def main():
	a = some_subclass(0)
	b = some_subclass(1)
	c = some_subclass(2) as C
	#cc = C(3)
	#cc = c as C  ## segfaults
	#print(cc.__class__)

	print(a.getclassname())  ## works
	print(b.getclassname())  ## works
	print(c.getclassname())  ## segfaults  - TODO fixme


	## TODO-FIXME
	print(a.method())
	print(b.method())
	print(c.method())
	''' above prints
	1
	2
	-810797173
	'''
	print('- - - - - - - ')
	if isinstance(b, B):
		print('b is type B')
		print(b.method())
		print(b.foo())
	if isinstance(c, C):
		print('c is type C')
		print(c.method())
		print(c.bar())
	else:
		print('error: c is not type C')
	#print(c.__class__)


	## TODO-FIXME
	# Segmentation fault
	#for i in range(3):
	#	o = some_subclass(i)
	#	print(o.method())
	#	if isinstance(o, B):
	#		print(o.foo())
	#	if isinstance(o,C):## TODO-FIX elif isinstance(o,C)
	#		print(o.bar())

