"""string basics"""

def main():
	TestError(len('a') == 1)
	a = 'XYZ'
	TestError( a[0] == 'X' )

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

	e = 'x%sx' %1
	TestError( e=='x1x' )