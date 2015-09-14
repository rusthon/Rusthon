from runtime import *
'''
range builtin
'''

def main():
	a = range(10)
	assert( a[0]==0 )
	assert( a[1]==1 )
	assert( len(a)==10 )

	b = range(1,10)
	assert( b[0]==1 )
	assert( b[1]==2 )
	assert( len(b)==9 )

	c = 0
	for i in range(10):
		c += 1
	assert( c == 10 )

	d = 0
	for i in range(1, 10):
		d += 1
	assert( d == 9 )

	e = 0
	for i in range(1, 8+2):
		e += 1
	assert( e == 9 )

main()
