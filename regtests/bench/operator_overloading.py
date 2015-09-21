'''
bretts simple operator overloading benchmark
'''

from time import clock
from runtime import *

def main():
	times = test( 3 )
	avg = sum(times) / len(times)
	print( avg )


class Vector:
	def __init__(self, x,y,z):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other):
		return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

	def __mul__(self, other):
		return Vector(self.x*other.x, self.y*other.y, self.z*other.z)


def benchmark(n):
	a = [ Vector(i*0.09,i*0.05, i*0.01) for i in range(n)]
	b = [ Vector(i*0.08,i*0.04, i*0.02) for i in range(n)]
	c = []
	d = []
	for j in range(n):
		with oo:
			u = a[j]
			v = b[j]
			c.append( u+v )
			d.append( u*v )

	return [c,d]

POINTS = 100000

def test(arg):	
	times = []
	for i in range(arg):
		t0 = clock()
		o = benchmark(POINTS)
		tk = clock()
		times.append(tk - t0)
	return times
	

main()