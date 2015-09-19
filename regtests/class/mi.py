from runtime import *
'''
multiple inheritance
'''
class A:
	def foo(self) -> int:
		return 1

class B:
	def bar(self) -> int:
		return 2

class C( A, B ):
	def call_foo_bar(self) -> int:
		a = self.foo()
		a += self.bar()
		return a

	## extend foo ##
	def foo(self) -> int:
		#a = A.foo(self)  ## TODO fix me, or support `super`
		a  = A.prototype.foo(self)  ## workaround
		a += 100
		return a

def main():
	a = A()
	assert( a.foo()==1 )
	b = B()
	assert( b.bar()==2 )

	c = C()
	assert( c.foo()==101 )
	assert( c.bar()==2 )

	assert( c.call_foo_bar()==103 )

main()
