"""compare"""

from runtime import *

def main():
	a = 'XYZ'
	b = 'XYZ'
	assert( a == b )

	x = False
	if 'a' < 'b':
		x = True

	assert( x==True )

	assert( 'a' < 'b' )

main()