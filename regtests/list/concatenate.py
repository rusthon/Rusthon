"""concatenate lists"""

def main():
	a = [1,2]
	b = [3,4]
	c = a + b

	TestError( len(c)==4 )
	TestError( c[0]==1 )
	TestError( c[1]==2 )
	TestError( c[2]==3 )
	TestError( c[3]==4 )
