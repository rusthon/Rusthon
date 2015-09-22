'''
float numbers
'''

from time import clock
from math import sin, cos, sqrt
from runtime import *

def main():
	times = test( 3 )
	avg = sum(times) / len(times)
	print( avg )


#class Point(object):  ## not allowed in RapydScript
class Point:
	def __init__(self, i):
		self.x = sin(i)
		self.y = cos(i) * 3
		self.z = (self.x * self.x) / 2

	def __repr__(self):
		return "Point: x=%s, y=%s, z=%s" % (self.x, self.y, self.z)

	def normalize(self):
		norm = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
		self.x /= norm
		self.y /= norm
		self.z /= norm

	def maximize(self, other):
		if self.x < other.x: self.x = other.x
		if self.y < other.y: self.y = other.y
		if self.z < other.z: self.z = other.z
		return self


def maximize(points):
	next = points[0]
	for p in points[1:]:
		next = next.maximize(p)
	return next

def benchmark(n):
	points = [None] * n
	for i in range(n):
		points[i] = Point(i)
	for p in points:
		p.normalize()
	return maximize(points)

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