'''
generics classes with common base.
'''
class A:
	def __init__(self, x:int):
		let self.x : int = x
		let self.z : int = 0


	def some_subclass( self, o:A, s:bool ) -> self:
		#if s:
		#	## forces the return type to be self, if the result from this method is an assignment
		#	## then a switch is generated, and the function body is put into each case,
		#	## this allow methods to work on the returned instance.
		#	return go.type_assert(o, self)
		#else:
		## TODO fixme
		return self

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


def main():
	a = A( 1000 )
	b = B()
	c = C()

	assert a.x == a.bar()

	x = my_generic( a )
	assert a.x == x

	y = my_generic( b )
	assert y==11

	z = my_generic( c )
	assert z==201

	assert b.z==1
	assert c.z==100


	## calling a method that has returns multiple subclasses with the result assigned to variable
	## will generate a switch that enables methods
	#w = 0
	## tests returning self
	bb = b.some_subclass(b, false)
	w = bb.bar()
	assert w==y
	cc = c.some_subclass(b, false)
	w = cc.bar()
	assert w==z


	## tests returning the other subclass type
	ccc = b.some_subclass(c, true)
	w = ccc.bar()
	assert w==z

	bbb = c.some_subclass(b, true)
	w = bbb.bar()
	assert w==y


	## Gotchas ##

	## calls B.bar(), my_generic still works when b returns self,
	## if C is returned, then my_generic breaks.
	w = my_generic( b.some_subclass(c, false) )
	#print(w)
	assert w == y


	## reassignment to bb type of *B should be allowed, because this works at runtime, but goc throws an error,
	## because it thinks that c.some_subclass can only return *C, and `bb` above got retyped as *B.
	#bb = c.some_subclass(b, true)
	d = c.some_subclass(b, true)
	w = d.bar()
	assert w==y


	print('----------no panics----------')