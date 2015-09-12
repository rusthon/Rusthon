"""string multiplication"""
from runtime import *

def main():
	print 'testing string multiplication'
	assert 'hi'*2 == 'hihi'
	a = 'hi'

	## this fails because `a` is not a string literal,
	## operator overloading must be used for this to work.
	#assert a*2 == 'hihi'

	with oo:
		b = a * 2

	assert( b == 'hihi' )

	## you can also be verbose, and use `__mul__` directly
	assert a.__mul__(2) == 'hihi'
	print 'OK'

main()