'''
generics classes with common base.
'''
class A:
	def __init__(self, x:int):
		int self.x = x
		int self.z = 0

	def bar(self) -> int:
		return self.x

	def foo( self, o:A, s:bool ) -> self:
		if s:
			return go.type_assert(o, self)
		else:
			return self

class B(A):
	def __init__(self):
		A.__init__(self, 10)
		int self.z = 1

	def bar(self) ->int:
		print('calling B.bar')
		return self.x + self.z

class C(A):
	def __init__(self):
		A.__init__(self, 100)
		int self.z = 100
		int self.w = 1

	def bar(self) ->int:
		print('calling C.bar')
		return self.x + self.z + self.w


def my_generic( g:A ) ->int:
	return g.bar()

def main():
	a = A( 1000 )
	b = B()
	c = C()

	TestError(a.x == a.bar() )
	TestError(a.x == a.foo(a,false).bar() )

	x = my_generic( a )
	TestError(a.x == x )

	y = my_generic( b )
	TestError( y==11 )

	z = my_generic( c )
	TestError( z==201 )

	TestError( b.z==1 )
	TestError( c.z==100 )

	w = b.bar()
	#print(w)

	bb = b.foo(b, false)
	w = bb.bar()
	TestError(w==y)

	print('testing C returned from B.foo')
	w = b.foo(c, true).bar()
	print(b.foo(c, true).w)
	TestError(w==z)


	cc = c.foo(b, false)
	w = cc.bar()
	TestError(w==z)

	## reassignment to bb type of *B should be allowed, because this works at runtime, but goc throws an error,
	## because it thinks that c.foo can only return *C
	#bb = c.foo(b, true)
	d = c.foo(b, true)
	w = d.bar()
	TestError(w==y)

	w = my_generic( b.foo(c, false) )  ## calls B.bar()
	#print(w)
	TestError( w == y )

	w = my_generic( b.foo(c, true) )   ## calls C.bar()
	print(w)
	TestError( w == z )

	print('testing B returned from C.foo')
	u = c.foo(b, true)
	print(u.x)
	print(u.z)
	print(u.w)
	w = my_generic( u )   ## calls B.bar()
	print(w)
	print(y)
	TestError( w==y )