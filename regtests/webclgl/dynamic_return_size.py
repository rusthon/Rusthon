class myclass:
	def __init__(self):
		self.width = 100
		self.height = 64
		self.step = 0.01

	def run(self, w, h, s, retw, reth):
		self.width = w
		self.height = h
		self.step = s

		@returns( array=[retw,reth] )
		@gpu.main
		def gpufunc():
			float b = 0.0
			for x in range( self.width ):
				for y in range( self.height ):
					b += self.step
			return b

		return gpufunc()

def main():
	A = myclass()
	r = A.run(4,4, 0.8, 16,128)
	TestError( len(r)==128 )
	TestError( len(r[0])==16 )
	r = A.run(16,16, 0.5, 64,16)
	TestError( len(r[0])==64 )
	TestError( len(r)==16  )
