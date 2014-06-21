"""iterate over dynamic list"""
from random import random

class G:
	def __init__(self, s):
		self.arr1 = [ random() for i in range(s) ]

	def run(self, X):

		@returns( array=[8,8] )
		@gpu.main
		def gpufunc(x):
			float x
			float* a = self.arr1
			#return float( len(a) ) *0.1  ## this also works
			float b = x * 0.5
			for i in range( len(a) ):
				b += a[i]
			return b

		return gpufunc(X)


def main():
	u = -1.0
	g = G(64)
	res = g.run( u )
	print(res)
	for i in range(3):  ## test dynamic size
		if i==0:
			g.arr1 = [ 0.01 for x in range(8) ]
		elif i==1:
			g.arr1 = [ 0.01 for x in range(16) ]
		else:
			g.arr1 = [ 0.01 for x in range(32) ]

		res = g.run( u )
		print(res)