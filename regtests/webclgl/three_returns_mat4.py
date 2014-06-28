'''@gpu class three.js'''
import three

gpu.object( three.Matrix4, 'mat4', 'elements')

@gpu.object
class MyObject:
	@gpu.method
	def mymethod(self, other) -> mat4:
		mat4 other
		return self.mat * other

	def __init__(self, x,y,z):
		self.mat = new( three.Matrix4() )
		print('THREE mat4')
		print(self.mat)



class myclass:
	def run(self, w):
		self.array = [ MyObject( 1.1, 1.2, 1.3 ) for x in range(w) ]

		@typedef(o=MyObject)
		@gpu.main
		def gpufunc() -> mat4:
			struct* A = self.array
			mat4 b = mat4(1.0)
			#mat4 c = mat4(1.1)

			#for s in iter(A):
			#	b *= s.mymethod(c)

			o = A[...]
			return o.mymethod(b)

		for ob in self.array:
			gpufunc.matrices.append( ob.mat.elements )

		return gpufunc()

def main():
	m = myclass()
	r = m.run(16)
	print(r)
