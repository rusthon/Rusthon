'''
generics classes with common base.
'''
class A:
	def __init__(self, x:int):
		let self.x : int = x
		let self.z : int = 0


	def some_subclass( self, o:A, s:bool ) -> self:
		return o

	def bar(self) -> int:
		return self.x


class B(A):
	def __init__(self):
		A.__init__(self, 10)
		let self.z : int = 1

	def bar(self) ->int:
		#print('calling B.bar')
		#print(self.__class__)
		return self.x + self.z

class C(A):
	def __init__(self):
		A.__init__(self, 100)
		let self.z : int = 100
		let self.w : int = 1

	def bar(self) ->int:
		#print('calling C.bar')
		#print(self.__class__)
		return self.x + self.z + self.w


def my_generic( g:A ) ->int:
	return g.bar()


def mainx():
	a = A( 1000 )
	print a
	b = B()
	c = C()

	assert a.x == a.bar()

	x = my_generic( a )
	assert a.x == x

	y = my_generic( b )
	assert y==11

	z = my_generic( c )
	##z = my_generic( b.some_subclass(c,true) )  ## todo fixme
	assert z==201


	## calling a method that has returns multiple subclasses with the result assigned to variable
	## will generate a switch that enables methods

	## tests returning self
	bb = b.some_subclass(b, false)
	w = bb.bar()
	assert w==y

	cc = c.some_subclass(b, false)
	w = cc.bar()
	assert w==z


	## tests returning other
	ccc = b.some_subclass(c, true)
	w = ccc.bar()
	assert w==z

	bbb = c.some_subclass(b, true)
	w = bbb.bar()
	assert w==y
	assert my_generic(bbb)==y


def main():
	a = A( 1000 )
	b = B()
	c = C()
	print a

	## tests returning self
	bb = b.some_subclass(b, false)
	w = bb.bar()
	print w

	cc = c.some_subclass(b, false)
	w = cc.bar()


	## tests returning other
	ccc = b.some_subclass(c, true)
	w = ccc.bar()

	bbb = c.some_subclass(b, true)
	w = bbb.bar()
