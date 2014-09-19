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