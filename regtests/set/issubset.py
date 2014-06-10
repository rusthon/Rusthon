"""get/set remote attributes"""

def main():
	x = set([1,2,3])
	y = set([1,2,3,4])

	TestError( x.issubset(y)==True )
	TestError( y.issubset(x)==False )

	