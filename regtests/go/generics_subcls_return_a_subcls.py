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
		return self.x + self.z

class C(A):
	def __init__(self):
		A.__init__(self, 100)
		int self.z = 100

	def bar(self) ->int:
		return self.x + self.z


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
	TestError( z==200 )

	TestError( b.z==1 )
	TestError( c.z==100 )

	w = b.bar()
	print(w)


	## all of below breaks  ##

	bb = b.foo(c, false)
	w = bb.bar()
	print(w)

	w = my_generic( b.foo(c, false) )  ## calls B.bar()
	print(w)
	TestError( w == y )

	w = my_generic( b.foo(c, true) )   ## calls C.bar()
	TestError( w == z )

	w = my_generic( c.foo(b, true) )   ## calls B.bar()
	TestError( w==y )