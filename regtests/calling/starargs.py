from runtime import *
"""unpack starargs"""
def f(x, a, b, c):
	return x+a+b+c

def f2(x,y,z, w=0):
	return x+y+z+w

def main():
	a = [1,1,1]
	assert( f(1, *a) == 4)

	assert( f2(*a, w=10) == 13)

	b = [1,1]
	assert( f2(100, *b, w=10) == 112)

main()
