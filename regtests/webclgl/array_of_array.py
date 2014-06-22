class myclass:
	def __init__(self):
		pass

	def run(self, w, h, length):
		self.array = [ [x*y*0.5 for y in range(h)] for x in range(w) ]

		@returns( array=64 )
		@gpu.main
		def gpufunc():
			float* A = self.array
			float b = 0.0
			for subarray in A:
				for j in range( len(self.array[0]) ):
					b += subarray[j]
			return b

		return gpufunc()

def main():
	m = myclass()
	r = m.run(8,4)
	print(r)