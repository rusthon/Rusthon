'''stdlib array'''
from array import array

def main():
	a = array('i', [1,2,3])
	TestError( len(a)==3 )
	TestError( a[0]==1 )
	TestError( 3 in a )
	x = 0
	for y in a:
		x += y
	TestError( x == 6 )

	## this fails in javascript-mode because it is a raw typed array can not be resized
	#a.append( 4 )
	#TestError( len(a)==4 )


