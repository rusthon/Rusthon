"""setitem and append"""
def main():
	a = [1,2,3,4]
	idx = 1
	TestError( a[0]==1 )
	TestError( a[idx]==2 )

	a[ 0 ] = 'hello'
	a[ 1 ] = 'world'
	TestError( a[0]=='hello' )
	TestError( a[1]=='world' )

	a.append( 'xxx' )
	TestError( a[4]=='xxx' )
	TestError( len(a)==5 )

	a.append( 'yyy' )
	TestError( a[5]=='yyy' )
	TestError( len(a)==6 )
