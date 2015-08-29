"""function call"""
def f(a:int, b:int, c:int) ->int:
	print 'testing f: plain args'
	return a+b+c

def f2(a:int=1, b:int=2, c:int=3) ->int:
	print 'testing f2: keyword args'
	return a+b+c

def f3( *args:int ) ->int:
	print 'testing f3: star args'
	return args[0] + args[1] + args[2]


def main():
	assert f(1,2,3) == 6

	x = f2( b=100 )
	assert x==104

	arr = [1,2,3]
	y = f3( *arr )
	assert y==6