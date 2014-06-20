"""inline dynamic list"""
from random import random

class G:
	def __init__(self):
		self.pi = 7/22.0
		self.scale = 0.1
		self.arr1 = [ random() for i in range(4) ]
		self.arr2 = [ random()*0.01 for i in range(32) ]

		@returns( array=[16,16] )
		@gpu.main
		def gpufunc(x,y,z,w):
			float x
			float y
			float z
			float w
			float* a = self.arr1
			float m = self.scale
			a[3] = 0.5
			return a[0] * self.pi * m

		self.gpufunc = gpufunc


def main():
	g = G()
	res = g.gpufunc(0.1, 0.2, 0.3, 0.4)
	print(res)
