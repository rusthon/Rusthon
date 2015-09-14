from runtime import *
'''
list passed to function
'''

def f( m:map[string]int ):
	m['x'] = 100

def main():
	a = map[string]int{
		'x' : 1,
		'y' : 2,
		'z' : 3
	}
	assert( a['x']==1 )
	f( a )
	assert( a['x']==100 )
	#assert( len(a)==4 )
main()
