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


