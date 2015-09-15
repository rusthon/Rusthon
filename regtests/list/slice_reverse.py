from runtime import *
"""list reverse slice"""


def main():
	a = range(10)
	b = a[ 4::-1 ]

	#if BACKEND=='DART':
	#	print(b[...])
	#else:
	#	print(b)


	assert( b[0]==4 )
	assert( b[1]==3 )
	assert( b[2]==2 )
	assert( b[3]==1 )
	assert( b[4]==0 )

	c = range(20)
	d = c[ 2::-1 ]

	#if BACKEND=='DART':
	#	print(d[...])
	#else:
	#	print(d)

	assert( d[0]==2 )
	assert( d[1]==1 )
	assert( d[2]==0 )

main()
