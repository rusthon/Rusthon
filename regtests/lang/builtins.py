'''
builtin functions
'''


def main():
	n = float('1.1')
	TestError( n==1.1 )

	n = float('NaN')
	TestError( isNaN(n)==True )

	r = round( 1.1234, 2)
	#print(r)
	TestError( str(r) == '1.12' )

	r = round( 100.001, 2)
	TestError( r == 100 )

	i = int( 100.1 )
	TestError( i == 100 )

	r = round( 5.49 )
	TestError( r == 5 )

	r = round( 5.49, 1 )
	TestError( r == 5.5 )

