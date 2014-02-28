"""list slice"""
def main():
	a = range(10)[:-5]
	TestError( len(a)==5 )
	TestError( a[4]==4 )

	b = range(10)[::2]
	TestError( len(b)==5 )
	TestError( b[0]==0 )
	TestError( b[1]==2 )
	TestError( b[2]==4 )
	TestError( b[3]==6 )
	TestError( b[4]==8 )
