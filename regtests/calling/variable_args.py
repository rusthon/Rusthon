"""variable args"""
def f(a, *args):
	c = a
	for b in args:
		c += b
	return c

def main():
	## dart only supports up to a fixed number (16) of variable arguments
	TestError( f(1, 2, 3, 3) == 9)

