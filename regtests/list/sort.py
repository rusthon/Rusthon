"""list sort"""

def main():
	x = [100, 10, 3,2,1]
	x.sort()
	TestError( x[0]==1 )
	TestError( x[1]==2 )
	TestError( x[2]==3 )
	TestError( x[3]==10 )
	TestError( x[4]==100 )

	y = ['C', 'B', 'A']
	y.sort()
	TestError( y[0]=='A' )
	TestError( y[1]=='B' )
	TestError( y[2]=='C' )
