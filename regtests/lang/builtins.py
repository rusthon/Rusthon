'''
builtin functions
'''


def main():
	n = float('1.1')
	TestError( n==1.1 )

	n = float('NaN')
	TestError( isNaN(n)==True )


