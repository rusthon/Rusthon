"""list indices"""
def main():
	a = [1,2,3,4]
	idx = 1
	TestError( a[0]==1 )
	TestError( a[idx]==2 )
	TestError( a.index(3)==2 )
