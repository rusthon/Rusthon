from runtime import *
"""custom addition"""

class A:
	def __init__(self):
		self.x = 5
	def __add__(self, other):
		return self.x + other.x


def main():
	print 'testing __add__ operator overloading'
	a = A()
	b = A()
	with oo:
		c = a + b
	assert( c == 10 )
	print 'ok'

main()
