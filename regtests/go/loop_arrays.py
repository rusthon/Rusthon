'''
array loop
'''

def main():

	a = [1,2,3]
	y = 0
	for x in a:
		y += x
	TestError( y==6 )

	z = ''
	arr = ['a', 'b', 'c']
	for v in arr:
		z += v
	TestError( z == 'abc' )

	#b = False
	#if 'a' in arr:
	#	b = True
	#TestError( b == True )

	b = 0
	for i in range(10):
		b += 1
	TestError( b == 10 )

	c = ''
	d = 0
	for i,v in enumerate(arr):
		c += v
		d += i
	TestError( c == 'abc' )
