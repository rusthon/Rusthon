"""compare"""

def main():
	a = 'XYZ'
	b = 'XYZ'
	TestError( a == b )

	x = False
	if 'a' < 'b':
		x = True

	TestError( x==True )

	TestError( 'a' < 'b' )
