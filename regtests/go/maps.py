"""map types"""

def main():
	a = map[string]int{
		'x': 1,
		'y': 2,
		'z': 3,
	}

	#print( a['x'] )
	TestError( a['x']==1 )

	b = map[int]string{ 0:'a', 1:'b' }
	#print( b[0] )
	#print( b[1] )
	TestError( b[0]=='a' )
	TestError( b[1]=='b' )

	c = {'x':100, 'y':200}
	#print( c['x'] )
	#print( c['y'] )

	TestError( c['x']==100 )
	TestError( c['y']==200 )
