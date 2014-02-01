'''
generator function
'''

def fib(n):
	a, b = 0, 1
	for x in range(n):
		yield a
		a,b = b, a+b
	yield 'world'

def main():
	arr = []
	for n in fib(20):
		arr.append( n )

	TestError( arr[0]==0 )
	TestError( arr[1]==1 )
	TestError( arr[2]==1 )
	TestError( arr[3]==2 )
	TestError( arr[4]==3 )
	TestError( arr[5]==5 )
	TestError( arr[6]==8 )
	TestError( arr[7]==13 )
	TestError( arr[8]==21 )
	TestError( arr[9]==34 )
	TestError( arr[10]==55 )
