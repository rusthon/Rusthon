from runtime import *
"""list sort"""

def main():
	x = [100, 10, 3,2,1]
	x.sort()
	assert( x[0]==1 )
	assert( x[1]==2 )
	assert( x[2]==3 )
	assert( x[3]==10 )
	assert( x[4]==100 )

	y = ['C', 'B', 'A']
	y.sort()
	assert( y[0]=='A' )
	assert( y[1]=='B' )
	assert( y[2]=='C' )

main()
