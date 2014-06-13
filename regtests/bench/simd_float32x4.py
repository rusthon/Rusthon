"""simd float32x4 micro benchmark"""
from time import time

def main():
	start = time()
	float32x4 a = numpy.array( [1.0001, 1.0002, 1.0003, 1.0004], dtype=numpy.float32 )
	float32x4 b = numpy.array( [1.00009, 1.00008, 1.00007, 1.00006], dtype=numpy.float32 )
	float32x4 c = numpy.array( [1.00005, 1.00004, 1.00003, 1.00002], dtype=numpy.float32 )

	arr = []
	for i in range(20000):
		c *= a*b
		arr.append( a*b*c )

	print(time()-start)