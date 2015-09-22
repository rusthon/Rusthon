from runtime import *
"""variable keywords"""

def f2(**kw):
	a = 0
	for key in iter(kw):
		a += kw[key]
	return a

def main():

	assert( f2(x=1,y=2) == 3 )
main()
