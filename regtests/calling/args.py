from runtime import *
"""simple function call"""
def f(a, b, c):
	return a+b+c

def main():
	assert( f(1,2,3) == 6)


main()
