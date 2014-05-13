'''
range builtin
'''

def main():
	a = range(10)
	TestError( a[0]==0 )
	TestError( a[1]==1 )
	TestError( len(a)==10 )

	b = range(1,10)
	TestError( b[0]==1 )
	TestError( b[1]==2 )
	TestError( len(b)==9 )

	c = 0
	for i in range(10):
		c += 1
	TestError( c == 10 )

	d = 0
	for i in range(1, 10):
		d += 1
	TestError( d == 9 )

	e = 0
	for i in range(1, 8+2):
		e += 1
	TestError( e == 9 )
