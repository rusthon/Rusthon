from runtime import *
"""list.pop(n)"""


def main():
	a = list(range(10))
	print a
	b = a.pop()
	print b
	print a
	assert( b==9 )
	c = a.pop(0)
	assert( c==0 )

	d = ['A', 'B', 'C']
	assert( d.pop(1)=='B' )
	assert( len(d)==2 )
main()
