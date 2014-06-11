"""list reverse slice"""


def main():
	a = range(10)
	b = a[ 4::-1 ]

	#if BACKEND=='DART':
	#	print(b[...])
	#else:
	#	print(b)


	TestError( b[0]==4 )
	TestError( b[1]==3 )
	TestError( b[2]==2 )
	TestError( b[3]==1 )
	TestError( b[4]==0 )

	c = range(20)
	d = c[ 2::-1 ]

	#if BACKEND=='DART':
	#	print(d[...])
	#else:
	#	print(d)

	TestError( d[0]==2 )
	TestError( d[1]==1 )
	TestError( d[2]==0 )
