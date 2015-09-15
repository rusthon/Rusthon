from runtime import *
"""range"""
def main():
	a = range(10)
	assert( len(a)==10 )
	assert( a[0] == 0 )
	assert( a[9] == 9 )

	b = range(1,10)
	assert( len(b)==9 )
	assert( b[0] == 1 )
	assert( b[8] == 9 )


main()
