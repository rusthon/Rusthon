"""big array mult"""
from time import time
from random import random

ARRAY_SIZE = 1024*1024*4

@returns( array=ARRAY_SIZE )
@gpu.main
def myfunc(A, B, C, D):
	float* A
	float* B
	float* C
	float* D
	vec2 n = get_global_id()  ## WebCL API
	return A[n] * B[n] * C[n] * D[n]

def main():

	a = [ random() for i in range(ARRAY_SIZE)]
	b = [ random() for i in range(ARRAY_SIZE)]
	c = [ random() for i in range(ARRAY_SIZE)]
	d = [ random() for i in range(ARRAY_SIZE)]

	if PYTHON=='PYTHONJS':
		start = time()
		res = myfunc( a,b,c,d )
		#print(res)
		print( time()-start )
	else:
		a = numpy.array(a, dtype=numpy.float32 )
		b = numpy.array(b, dtype=numpy.float32 )
		c = numpy.array(c, dtype=numpy.float32 )
		d = numpy.array(d, dtype=numpy.float32 )
		start = time()
		res = a * b * c * d
		print( time()-start )
