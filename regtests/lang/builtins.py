from runtime import *
'''
builtin functions
'''


def main():
	o = ord('x')
	assert( o == 120 )

	n = float('1.1')
	assert( n==1.1 )

	n = float('NaN')
	print( n )
	assert( isNaN(n)==True )

	r = round( 1.1234, 2)
	print(r)
	assert( str(r) == '1.12' )

	x = chr(120)
	print(x)
	assert x == 'x'

	r = round( 100.001, 2)
	assert( r == 100 )

	i = int( 100.1 )
	assert( i == 100 )

	r = round( 5.49 )
	assert( r == 5 )

	r = round( 5.49, 1 )
	assert( r == 5.5 )


main()
