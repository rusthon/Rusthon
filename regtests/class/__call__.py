"""custom callable"""
from runtime import *

class A:
	def __init__(self):
		self.x = 5

	def __call__(self):
		print self.x
		return 'XXX'

	def foo(self):
		return self.x


def main():
	print 'testing __call__'
	a = A()
	assert a.x == 5
	assert a() == 'XXX'
	assert a.__call__() == 'XXX'
	assert a.foo() == 5
	assert isinstance(a, A)
	print 'ok'

main()