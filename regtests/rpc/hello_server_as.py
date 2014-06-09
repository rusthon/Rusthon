"""simple rpc call"""

def f(v):
	return v * 2

def main():
	a = 'hello'
	b = 'server'
	x = 100
	y = 200
	with rpc('http://localhost:8080') as server:
		c = server.concat( a, b )
		z = server.add( x, y )
		w = f(z)

	TestError( c == 'helloserver' )
	TestError( z == 300 )
	TestError( w == 600 )

	