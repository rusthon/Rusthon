from runtime import *
'''
list comprehensions
'''

def main():
	a = [x for x in range(3)]
	assert( len(a)==3 )
	assert( a[0]==0 )
	assert( a[1]==1 )
	assert( a[2]==2 )

main()
