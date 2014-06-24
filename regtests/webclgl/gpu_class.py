'''@gpu class'''

@gpu.object
class MyObject:
	## below `self` is not `this` in javascript
	## `self` is a GLSL struct of MyObject
	@gpu.method
	float def subroutine(self, x,y):
		float x
		float y
		return x + y * self.attr2
	## subroutines must be defined ahead of where they are used

	@gpu.method
	float def mymethod(self, x,y):
		float x
		float y
		if self.index == 0:
			return -20.5
		elif self.index == 0:
			return 0.6
		else:
			return self.subroutine(x,y) * self.attr1


	## here `self` is javascript's `this`
	def __init__(self, a, b, i):
		self.attr1 = a
		self.attr2 = b
		self.index = int16(i)




class myclass:
	def run(self, w):
		self.array = [ MyObject( 1.1, 1.2, x ) for x in range(w) ]

		@returns( array=64 )
		@gpu.main
		def gpufunc():
			struct* A = self.array
			float b = 0.0

			for s in iter(A):
				b += s.mymethod(1.1, 2.2)

			return b

		return gpufunc()

def main():
	m = myclass()
	r = m.run(8)
	print(r)
