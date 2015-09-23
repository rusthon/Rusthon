from runtime import *
"""list slice set"""


def main():
	a = list(range(10))
	for v in a: print v
	a[ 2:4 ] = 'XXXY'
	#print a
	print '------------'
	for v in a:
		print v


	assert( a[0]==0 )
	assert( a[1]==1 )

	assert( a[2]=='X' )
	assert( a[3]=='X' )
	assert( a[4]=='X' )
	assert( a[5]=='Y' )

	assert( a[6]==4 )
	assert( a[7]==5 )
	assert( a[8]==6 )
	assert( a[9]==7 )
	assert( a[10]==8 )
	assert( a[11]==9 )

	b = list(range(3))
	#print b
	c = b [ :2 ]
	#print c
	assert( c[0]==0 )
	assert( c[1]==1 )
	print '----------'

	b[ :2 ] = 'ABC'
	assert( len(b)==4 )
	assert( b[0]=='A' )

	d = list(range(10))
	d[ 2:4 ] = [99, 100]
	assert( d[0]==0 )
	assert( d[1]==1 )
	assert( d[2]==99 )
	assert( d[3]==100 )

main()
