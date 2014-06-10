"""list.pop(n)"""


def main():
	a = list(range(10))
	b = a.pop()
	TestError( b==9 )
	c = a.pop(0)
	TestError( c==0 )

	d = ['A', 'B']
	TestError( d.pop(1)=='B' )
	TestError( len(d)==1 )