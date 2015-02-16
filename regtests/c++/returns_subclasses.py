'''
returns subclasses
'''
class A:
	def __init__(self, x:int):
		self.x = x
	def method(self) -> int:
		return self.x

class B(A):
	def foo(self) ->int:
		return self.x * 2

class C(A):
	def bar(self) ->int:
		return self.x + 200

class D(C):
	def hey(self) ->int:
		return self.x + 1


def some_subclass( x:int ) ->A:
	switch x:
		case 0:
			a = A(1)
			return a
		case 1:
			b = B(2)
			return b
		case 2:
			c = C(3)
			return c
		case 3:
			d = D(4)
			return d


def main():
	a = some_subclass(0)
	b = some_subclass(1)
	c = some_subclass(2)
	d = some_subclass(3)

	print(a.getclassname())
	print(b.getclassname())
	print(c.getclassname())
	print(d.getclassname())

	print(a.method())
	print(b.method())
	print(c.method())
	print(d.method())

	print('- - - - - - - ')
	if isinstance(b, B):
		print('b is type B')
		print(b.method())
		print(b.foo())
	else:
		print('error: b is not type B')

	if isinstance(c, C):
		print('c is type C')
		print(c.method())
		print(c.bar())
	else:
		print('error: c is not type C')

	if isinstance(d, D):
		print('d is type D')
		#print(d.bar())  ## TODO, subclass from C.
		print(d.hey())
	else:
		print('error: d is not type D')

	print('------------------')
	for i in range(3):
		o = some_subclass(i)
		print(o.method())
		if isinstance(o, B):
			print(o.foo())
		if isinstance(o,C):		## TODO-FIX elif isinstance(o,C)
			print(o.bar())

	print('end of test')