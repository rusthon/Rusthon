"""external method"""

class myclass:
	def __init__(self, i):
		self.index = i

	def get_index(self):
		return self.index

	def run(self, n):
		self.intarray = new(Int16Array(n))
		self.intarray[ self.index ] = 99

		@returns( array=n )
		@gpu.main
		def gpufunc():
			int* A = self.intarray

			## GLSL compile error: `Index expression must be constant`
			#int idx = self.get_index()
			#return float( A[idx] )
			
			return float( A[self.get_index()] )

		return gpufunc()

def main():
	m = myclass(10)
	r = m.run(64)
	print(r)
	TestError( int(r[10])==99 )