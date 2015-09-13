from runtime import *
"""variable args"""
def f(a, *args):
	print '*args'
	print args
	c = a
	for b in args:
		c += b
	return c

def main():
	print 'testing calling function that takes *args'
	assert( f(1, 2, 3, 3) == 9)
	print 'ok'

main()
