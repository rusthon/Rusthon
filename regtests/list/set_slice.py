from runtime import *
"""list slice set"""


def main():
	a = list(range(10))
	for v in a: print v
	a[ 2:4 ] = 'Y'
	print a
	print '------------'
	for v in a:
		print v

	assert( a[0]==0 )
	assert( a[1]==1 )

	assert( a[2]=='Y' )

	assert( a[3]==4 )
	assert( a[4]==5 )
	assert( a[5]==6 )
	assert( a[6]==7 )
	assert( a[7]==8 )
	assert( a[8]==9 )

	b = list(range(3))
	print b
	c = b [ :2 ]
	print c
	assert len(c)==2
	assert( c[0]==0 )
	assert( c[1]==1 )
	print '----------'
	print b
	b[ :2 ] = 'ABC'
	print b
	assert( len(b)==4 )
	assert( b[0]=='A' )
	assert( b[1]=='B' )
	assert( b[2]=='C' )
	assert b[3]==2

	e = range(5)
	print e
	e[ 2:3 ] = 'x'
	print e
	assert e[2]=='x'


	d = list(range(10))
	d[ 2:4 ] = [99, 100]
	assert( d[0]==0 )
	assert( d[1]==1 )
	assert( d[2]==99 )
	assert( d[3]==100 )
	print d

main()
