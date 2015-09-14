from runtime import *
"""get/set remote attributes"""

def main():
	x = set([1,2,3])
	y = set([1,2,3,4])

	assert( x.issubset(y)==True )
	assert( y.issubset(x)==False )

	
main()
