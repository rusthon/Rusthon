from runtime import *
'''
generator function, requires javascript ES6.
'''

def fib(n:int) -> int:
	a = 0
	b = 1
	c = 0

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

	assert( arr[0]==0 )
	assert( arr[1]==1 )
	assert( arr[2]==1 )
	assert( arr[3]==2 )
	assert( arr[4]==3 )
	assert( arr[5]==5 )
	assert( arr[6]==8 )
	assert( arr[7]==13 )
	assert( arr[8]==21 )
	assert( arr[9]==34 )
	assert( arr[10]==55 )

main()
