"""string basics"""

from runtime import *

def main():
	assert(len('a') == 1)
	a = 'XYZ'
	assert( a[0] == 'X' )
	assert( a[-1] == 'Z' )
	assert( a[0:2] == 'XY' )
	assert( a[:2] == 'XY' )
	assert( a[1:3] == 'YZ' )
	assert( a[1:] == 'YZ' )
	assert( a[-3:-1] == 'XY' )

	assert( a.lower() == 'xyz' )
	b = 'abc'
	assert( b.upper() == 'ABC' )

	assert( ord('A') == 65 )
	assert( chr(65) == 'A' )

	c = '%s-%s' %('xxx', 'yyy')
	assert( c == 'xxx-yyy' )

	d = 'a b c'.split()
	assert( d[0]=='a' )
	assert( d[1]=='b' )
	assert( d[2]=='c' )

	d = 'a,b,c'.split(',')
	assert( d[0]=='a' )
	assert( d[1]=='b' )
	assert( d[2]=='c' )

	e = 'x%sx' %1
	assert( e=='x1x' )

	f = 'x"y'
	assert( ord(f[1]) == 34 )

	f = 'x\"y'
	assert( ord(f[1]) == 34 )

	f = 'x\'y"'
	assert( ord(f[1]) == 39 )

	f = '\r'
	assert( ord(f[0]) == 13 )

main()