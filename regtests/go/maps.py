"""map types"""

def main():
	a = map[string]int{
		'x': 1,
		'y': 2,
		'z': 3,
	}

	print( a['x'] )

	b = map[int]string{ 0:'a', 1:'b' }
	print( b[0] )
	print( b[1] )