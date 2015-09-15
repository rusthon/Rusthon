"""basics"""
from runtime import *

def main():
	a = [1,2,3,4]
	assert( len(a)==4 )

	b = list()
	assert( len(b)==0 )
	b.append( 5 )
	assert len(b)==1

	with oo:
		a += b
	assert len(a)==5

	## the pythonic way
	a.extend( b )
	assert len(a)==6

main()