"""function call"""
def f(a:int, b:int, c:int) ->int:
	return a+b+c

def main():
	TestError( f(1,2,3) == 6)

