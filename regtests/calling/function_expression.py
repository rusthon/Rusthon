"""func expr"""

F = function( x,y ):
	return x+y

def main():
	TestError( F(1,2) == 3 )

