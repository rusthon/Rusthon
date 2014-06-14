"""simd float32vec micro benchmark"""
from time import time
from random import random

## SIMD in dart broken down into multiple float32x4 instances, with multiply implemented by looping
## over each element is slower than CPython with NumPy for an array larger than 32 elements.
## 64 elements runs about half the speed of NumPy in CPython.

def main():
	ARRAY_SIZE = 32  ## note, size must be divisible by 4
	x = []
	y = []
	z = []
	for i in range( ARRAY_SIZE ):
		x.append( random()+0.5 )
		y.append( random()+0.5 )
		z.append( random()+0.5 )

	a = numpy.array( x, dtype=numpy.float32 )
	b = numpy.array( y, dtype=numpy.float32 )
	c = numpy.array( z, dtype=numpy.float32 )

	## start benchmark
	start = time()

	arr = []
	for i in range(20000):
		arr.append( a*b*c )

	print(time()-start)