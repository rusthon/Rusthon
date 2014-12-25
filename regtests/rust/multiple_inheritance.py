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
		let mut a = self.foo()
		a += self.bar()
		return a

	def foo(self) -> int:
		return 100
	def bar(self) -> int:
		return 200

	def test_parents(self) -> int:
		#return A.foo(self) + B.bar(self)  ## this also  works
		return A.foo() + B.bar()


def main():
	a = A()
	TestError( a.foo()==1 )
	b = B()
	TestError( b.bar()==2 )

	c = C()
	TestError( c.foo()==100 )
	TestError( c.bar()==200 )

	TestError( c.call_foo_bar()==300 )
	TestError( c.test_parents()==3 )