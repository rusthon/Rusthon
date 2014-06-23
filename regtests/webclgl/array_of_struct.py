class myclass:
	def __init__(self, s):
		self.s = s
	def my_method(self):
		return self.s

	def run(self, w):
		self.array = [ {'myattr':1.1} for x in range(w) ]

		@returns( array=64 )
		@gpu.main
		def gpufunc():
			struct* structs = self.array
			float b = self.my_method()

			for structure in iter(structs):
				b += structure.myattr
			return b

		return gpufunc()

def main():
	m = myclass( 0.1 )
	r = m.run(8)
	print(r)