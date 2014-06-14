"""simd float32vec"""

def get_data():
	return [1.9, 1.8, 1.7, 0.6, 0.99,0.88,0.77,0.66]
def main():
	## the translator knows this is a float32vec because there are more than 4 elements
	x = y = z = w = 22/7
	a = numpy.array( [1.1, 1.2, 1.3, 0.4, x,y,z,w], dtype=numpy.float32 )

	## in this case the translator is not sure what the length of `u` is, so it defaults
	## to using a float32vec.
	u = get_data()
	b = numpy.array( u, dtype=numpy.float32 )

	c = a + b
	print(c)

	TestError( c[0]==3.0 )
	TestError( c[1]==3.0 )
	TestError( c[2]==3.0 )
	TestError( c[3]==1.0 )
