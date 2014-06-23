"""integer array"""

class myclass:
	def __init__(self):
		pass
	def run(self, n):
		self.intarray = new(Int16Array(n))
		self.intarray[0] = 100
		@returns( array=n )
		@gpu.main
		def gpufunc():
			int* A = self.intarray
			return float( A[0] )

		return gpufunc()

def main():
	m = myclass()
	r = m.run(64)
	print(r)
	TestError( int(r[0])==100 )