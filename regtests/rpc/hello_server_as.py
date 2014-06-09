"""simple rpc call"""

def main():
	a = 'hello'
	b = 'server'
	x = 100
	y = 200
	with rpc('http://localhost:8080') as server:
		c = server.concat( a, b )
		z = server.add( x, y )

	TestError( c == 'helloserver' )
	TestError( z == 300 )

	