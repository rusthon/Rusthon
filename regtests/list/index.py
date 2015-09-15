from runtime import *
"""list indices"""
def main():
	a = [1,2,3,4]
	idx = 1
	assert( a[0]==1 )
	assert( a[idx]==2 )
	assert( a.index(3)==2 )

main()
