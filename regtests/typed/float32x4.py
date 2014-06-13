"""simd float32x4"""

def main():
	float32x4 a = numpy.array( [1.1, 1.2, 1.3, 0.4], dtype=numpy.float32 )
	float32x4 b = numpy.array( [1.9, 1.8, 1.7, 0.6], dtype=numpy.float32 )

	c = a + b
	print(c)

	if PYTHON == 'PYTHONJS':
		TestError( c.x==3.0 )
		TestError( c.y==3.0 )
		TestError( c.z==3.0 )
		TestError( c.w==1.0 )

	else:
		TestError( c[0]==3.0 )
		TestError( c[1]==3.0 )
		TestError( c[2]==3.0 )
		TestError( c[3]==1.0 )
