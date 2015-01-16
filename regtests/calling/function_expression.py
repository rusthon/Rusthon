"""func expr"""

F = def ( x:int, y:int ) -> int:
	return x+y

def main():
	TestError( F(1,2) == 3 )

	funcs = [2]func(int,int)(int)()

	funcs[0] = def (x:int, y:int) -> int:
		return x-y

	funcs[1] = def (x:int, y:int) -> int:
		return x*y
