"""function call"""
def f(a:int, b:int, c:int) ->int:
	return a+b+c

def f2(a:int=1, b:int=2, c:int=3) ->int:
	return a+b+c

def f3( *args:int ) ->int:
	return args[0] + args[1] + args[2]


def main():
	TestError( f(1,2,3) == 6)

	x = f2( b=100 )
	TestError(x==104)

	arr = [1,2,3]
	y = f3( *arr )
	TestError( y==6 )