from runtime import *
"""setitem and append"""
def main():
	a = [1,2,3,4]
	idx = 1
	assert( a[0]==1 )
	assert( a[idx]==2 )

	a[ 0 ] = 'hello'
	a[ 1 ] = 'world'
	assert( a[0]=='hello' )
	assert( a[1]=='world' )

	a.append( 'xxx' )
	assert( a[4]=='xxx' )
	assert( len(a)==5 )

	a.append( 'yyy' )
	assert( a[5]=='yyy' )
	assert( len(a)==6 )

main()
