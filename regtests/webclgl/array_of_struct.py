'''array of structs'''
from random import random

class myclass:
	def __init__(self, a): self.a = a
	def my_method(self): return self.a

	def new_struct(self, g):
		return {
			'attr1' : 0.6 + g,
			'attr2' : 0.4 + g
		}


	def run(self, w):
		self.array = [ self.new_struct( x ) for x in range(w) ]

		@returns( array=64 )
		@gpu.main
		def gpufunc():
			struct* A = self.array
			float b = self.my_method()

			for s in iter(A):
				b += s.attr1 + s.attr2
			return b

		return gpufunc()

def main():
	f = 0.1234
	m = myclass( f )
	r = m.run(8)
	print(r)
	t = round(r[0]-64.0, 4)
	print(t)
	f = round(f, 4)
	print(f)
	ok = f==t
	print('test passed: %s' %ok )
	#TestError( f==t )