"""array types"""

def main():
	a = []int(1,2,3)
	TestError( a[0]==1 )
	TestError( len(a)==3 )

	b = [2]int(100,200)
	TestError( b[0]==100 )
	TestError( b[1]==200 )

	c = a[:2]
	TestError( len(c)==2 )