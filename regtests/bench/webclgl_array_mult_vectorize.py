"""big array mult"""
from time import time
from random import random

@gpu.vectorize
def array_mult(a,b,c,d):
	a = numpy.array(a, dtype=numpy.float32 )
	b = numpy.array(b, dtype=numpy.float32 )
	c = numpy.array(c, dtype=numpy.float32 )
	d = numpy.array(d, dtype=numpy.float32 )
	return a * b * c * d


def main():
	ARRAY_SIZE = 1024*1024*2

	a = [ random() for i in range(ARRAY_SIZE)]
	b = [ random() for i in range(ARRAY_SIZE)]
	c = [ random() for i in range(ARRAY_SIZE)]
	d = [ random() for i in range(ARRAY_SIZE)]

	start = time()
	res = array_mult( a,b,c,d )
	print( time()-start )
	#print(res)
