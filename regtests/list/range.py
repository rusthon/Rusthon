"""range"""
def main():
	a = range(10)
	TestError( len(a)==10 )
	TestError( a[0] == 0 )
	TestError( a[9] == 9 )

	b = range(1,10)
	TestError( len(b)==9 )
	TestError( b[0] == 1 )
	TestError( b[8] == 9 )

