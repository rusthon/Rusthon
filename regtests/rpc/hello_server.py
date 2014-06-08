"""simple rpc call"""

def main():
	a = 'hello'
	b = 'server'
	x = 100
	y = 200
	with rpc('http://localhost:8080'):
		c = concat( a, b )
		z = add( x, y )

	TestError( c == 'helloserver' )
	TestError( z == 300 )

	