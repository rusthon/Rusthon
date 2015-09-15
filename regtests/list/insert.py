from runtime import *
"""insert"""
def main():
	a = [1,2,3,4]
	assert( len(a)==4 )

	a.insert(0, 'hi')
	assert( len(a)==5 )
	assert( a[0]=='hi' )

	a.insert(1, a.pop(0))
	assert( a[0]==1 )
	assert( a[1]=='hi' )

main()
