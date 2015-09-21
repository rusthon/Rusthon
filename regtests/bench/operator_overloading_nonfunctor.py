'''
bretts simple operator overloading benchmark
'''

from time import clock
from runtime import *

def main():
	times = test( 3 )
	avg = sum(times) / len(times)
	print( avg )

UID = 0
class Vector:
	def __init__(self, x,y,z):
		global UID
		UID += 1
		self.id = UID
		self.x = x
		self.y = y
		self.z = z

	def add(self, other):
		return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

	def mul(self, other):
		return Vector(self.x*other.x, self.y*other.y, self.z*other.z)

	def call(self):
		return self.id

def benchmark(n):
	a = [ Vector(i*0.09,i*0.05, i*0.01) for i in range(n)]
	b = [ Vector(i*0.08,i*0.04, i*0.02) for i in range(n)]
	c = {}
	for j in range(n):
		u = a[j]
		v = b[j]
		c[u.call()] = u.add(v)
		c[v.call()] = u.mul(v)
	return c

POINTS = 10000

def test(arg):	
	times = []
	for i in range(arg):
		t0 = clock()
		o = benchmark(POINTS)
		tk = clock()
		times.append(tk - t0)
	return times
	

main()