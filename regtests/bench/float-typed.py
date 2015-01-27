'''
float numbers
'''

from time import clock
from math import sin, cos, sqrt

POINTS = 100000

class Point(object):

	def __init__(self, i:float):
		let self.x:float = sin(i)
		let self.y:float = cos(i) * 3
		let self.z:float = (self.x * self.x) / 2

	def normalize(self) ->self:
		norm = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
		self.x /= norm
		self.y /= norm
		self.z /= norm
		return self

	def maximize(self, other:Point ):
		if self.x < other.x: self.x = other.x
		if self.y < other.y: self.y = other.y
		if self.z < other.z: self.z = other.z


def maximize( points:[]Point ) ->Point:
	next = points[0]
	slice = points[1:]
	for p in slice:
		next = next.maximize(p)
	return next

def benchmark( n:int ) -> Point:
	points = []Point( 
		Point(i as float).normalize() for i in range(n) 
	)
	return maximize(points)


def test( arg:int ) ->[]float:
	times = []
	for i in range(arg):
		t0 = clock()
		o = benchmark(POINTS)
		tk = clock()
		times.append(tk - t0)
	return times
	
def main():
	times = test( 3 )
	avg = sum(times) / len(times)
	print( avg )
