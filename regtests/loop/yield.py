'''
generator function
'''

def fib(n:int) -> int:
	int a = 0
	int b = 1
	int c = 0

	for x in range(n):
		#print('looping')
		yield a
		c = b
		b = a+b
		a = c

	yield -1  ## signals end

def main():
	arr = []int()
	for n in fib(20):
		#print(n)
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
