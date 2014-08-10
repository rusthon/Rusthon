"""function call"""
def f(a:int, b:int, c:int) ->int:
	return a+b+c

def f2(a:int=1, b:int=2, c:int=3) ->int:
	return a+b+c


def main():
	TestError( f(1,2,3) == 6)

	x = f2( b=100 )
	TestError(x==104)
