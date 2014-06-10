"""insert"""
def main():
	a = [1,2,3,4]
	TestError( len(a)==4 )

	a.insert(0, 'hi')
	TestError( len(a)==5 )
	TestError( a[0]=='hi' )

	a.insert(1, a.pop(0))
	TestError( a[0]==1 )
	TestError( a[1]=='hi' )
