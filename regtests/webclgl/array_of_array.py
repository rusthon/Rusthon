class myclass:
	def __init__(self, s):
		self.s = s
	def my_method(self):
		return self.s

	def run(self, w, h):
		self.array = [ [x*y*0.5 for y in range(h)] for x in range(w) ]

		@returns( array=64 )
		@gpu.main
		def gpufunc():
			float* A = self.array
			float b = self.my_method()

			for subarray in A:
				for j in range( len(self.array[0]) ):
					b += subarray[j]
			return b

		return gpufunc()

def main():
	m = myclass( 0.1 )
	r = m.run(8,4)
	print(r)