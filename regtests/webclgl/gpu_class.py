'''@gpu class'''

@gpu.object
class MyObject:
	## below `self` is not `this` in javascript
	## `self` is a GLSL struct of MyObject
	@gpu.method
	float def mymethod(self, x,y):
		float x
		float y
		return self.subroutine(x,y) * self.attr1

	@gpu.method
	float def subroutine(self, x,y):
		float x
		float y
		return x + y

	## here `self` is javascript's `this`
	def __init__(self, a, b):
		self.attr1 = a
		self.attr2 = b




class myclass:
	def new_struct(self, a, b):
		return MyObject( a, b )

	def run(self, w):
		self.array = [ self.new_struct( x, 1.1 ) for x in range(w) ]

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
