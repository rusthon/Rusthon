"""func expr"""

F = def ( x:int, y:int ) -> int:
	return x+y

def main():
	TestError( F(1,2) == 3 )

