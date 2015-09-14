from runtime import *
'''
list passed to function
'''

def f( l:[]int ):
	l.append(1)

def main():
	a = []int(1,2,3)
	assert( a[0]==1 )
	f( a )
	assert( len(a)==4 )

	b = [ x for x in range(9) ]
	f( b )
	assert( len(b)==10 )

main()
