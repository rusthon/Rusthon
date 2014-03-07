'''
simple for loop
'''

def main():
	a = [1,2,3]
	y = 0
	for x in a:
		y += x
	TestError( y==6 )

	b = range(3)
	z = 0
	for x in b:
		z += x
	TestError( z==3 )

	w = 0
	for i in a:
		for j in b:
			w += 1
	TestError( w==9 )
