'''struct with array'''
from random import random

class myclass:

	def new_struct(self, g):
		return {
			'num' : g,
			'arr' : [0.1 for s in range(6)]
		}


	def run(self, w):
		self.array = [ self.new_struct( x ) for x in range(w) ]

		@returns( array=64 )
		@gpu.main
		def gpufunc():
			struct* A = self.array
			float b = 0.0

			for s in iter(A):
				b += s.num
				for i in range(len(s.arr)):
					b += s.arr[i]

				## note: assignment of a struct's array member to a variable is not allowed
				#float* a = s.arr  ## not allowed


			return b

		return gpufunc()

def main():
	m = myclass()
	r = m.run(8)
	print(r)
