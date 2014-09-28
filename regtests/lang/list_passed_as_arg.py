'''
list passed to function
'''

def f( l:[]int ):
	l.append(1)

def main():
	a = []int(1,2,3)
	TestError( a[0]==1 )
	f( a )
	TestError( len(a)==4 )

	b = []int( x for x in range(9) )
	f( b )
	TestError( len(b)==10 )
