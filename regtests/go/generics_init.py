'''
passing generic attribute to method
'''
class BaseA:
	def __init__(self, x:int, g:BaseX):
		int self.x = x
		self.g = g

	def foo( self ) -> self:
		return self.bar( self.g )

	def bar(self, g:BaseX) -> self:
		if g.flag:
			return go.type_assert(g.ob, self)
		else:
			return self


class B( BaseA ): pass
class C( BaseA ): pass

class BaseX:
	def __init__(self, f:bool):
		bool self.flag = f
		self.ob = None

	#def get(self) ->BaseA:
	#S	return self.ob

class X( BaseX ): pass
class Y( BaseX ): pass


def main():
	x = X(true)
	y = Y(false)
	b1 = B(1, x)
	b2 = B(2, y)

	x.ob = b2
	y.ob = b1

	print( b1.foo() )