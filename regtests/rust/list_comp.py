'''
rust list comprehensions
'''

#def F( arr:[]int ):
#	arr.append( 3 )

def main():
	a = []int(x for x in range(3))
	TestError( len(a)==3 )
	#F( a )
	#TestError( len(a)==4 )
	TestError( a[0]==0 )
	TestError( a[1]==1 )
	TestError( a[2]==2 )
	#TestError( a[3]==3 )
