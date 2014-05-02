"""string basics"""

def main():
	TestError(len('a') == 1)
	a = 'XYZ'
	TestError( a[0] == 'X' )
	TestError( a[-1] == 'Z' )
	TestError( a[0:2] == 'XY' )
	TestError( a[:2] == 'XY' )
	TestError( a[1:3] == 'YZ' )
	TestError( a[1:] == 'YZ' )
	TestError( a[-3:-1] == 'XY' )

	TestError( a.lower() == 'xyz' )
	b = 'abc'
	TestError( b.upper() == 'ABC' )

	TestError( ord('A') == 65 )
	TestError( chr(65) == 'A' )

	c = '%s-%s' %('xxx', 'yyy')
	TestError( c == 'xxx-yyy' )

	d = 'a b c'.split()
	TestError( d[0]=='a' )
	TestError( d[1]=='b' )
	TestError( d[2]=='c' )

	d = 'a,b,c'.split(',')
	TestError( d[0]=='a' )
	TestError( d[1]=='b' )
	TestError( d[2]=='c' )

	e = 'x%sx' %1
	TestError( e=='x1x' )

	f = 'x"y'
	TestError( ord(f[1]) == 34 )

	f = 'x\"y'
	TestError( ord(f[1]) == 34 )

	f = 'x\'y"'
	TestError( ord(f[1]) == 39 )

	f = '\r'
	TestError( ord(f[0]) == 13 )

