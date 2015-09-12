from runtime import *
"""keywords"""
def f(a, b=None, c=None):
	return (a+b) * c


def main():
	print 'testing keywords'
	print f(1, b=2, c=3)
	print f(1, c=3, b=2)
	assert( f(1, b=2, c=3) == 9)
	assert( f(1, c=3, b=2) == 9)
	print 'ok'
main()
