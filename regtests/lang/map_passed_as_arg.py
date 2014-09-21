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
	TestError( a['x']==1 )
	f( a )
	TestError( a['x']==100 )
	#TestError( len(a)==4 )