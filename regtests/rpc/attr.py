"""get/set remote attributes"""

def main():
	x = None
	y = None
	with rpc('http://localhost:8080') as server:
		server.A = 'hi'
		server.B = 100
		x = server.A
		y = server.B

	TestError( x == 'hi' )
	TestError( y == 100 )

	