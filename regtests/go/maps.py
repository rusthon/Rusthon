"""map types"""

def main():
	a = map[string]int{
		'x': 1,
		'y': 2,
		'z': 3,
	}

	print( a['x'] )
	assert a['x']==1

	b = map[int]string{ 0:'a', 1:'b' }
	print( b[0] )
	print( b[1] )
	assert b[0]=='a'
	assert b[1]=='b'

	## infers type of key and value ##
	c = {'x':100, 'y':200}
	print( c['x'] )
	print( c['y'] )

	assert c['x']==100
	assert c['y']==200 
