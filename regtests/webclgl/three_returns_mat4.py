'''@gpu class three.js'''
import three

gpu.object( three.Matrix4, 'mat4', 'elements')

@gpu.object
class MyObject:
	@gpu.method
	def mymethod(self, other) -> mat4:
		mat4 other
		return self.mat * other

	def __init__(self, x):
		self.mat = new( three.Matrix4() )
		print('THREE mat4')
		print(dir(self.mat))
		for i in range(16):
			self.mat.elements[i] = i*10
		self.mat.multiplyScalar(x)




class myclass:
	def run(self, w):
		self.array = [ MyObject( x+1.0 ) for x in range(w) ]

		@typedef(o=MyObject)
		@gpu.main
		def gpufunc() -> mat4:
			struct* A = self.array
			mat4 b = mat4(1.0)
			#mat4 c = mat4(1.1)

			#for s in iter(A):
			#	b *= s.mymethod(c)

			o = A[...]  ## gets the current index in gpufunc.return_matrices
			return o.mat #.mymethod(b)

		for ob in self.array:
			gpufunc.return_matrices.append( ob.mat.elements )

		return gpufunc()

def main():
	m = myclass()
	r = m.run(8)
	for a in r:
		print(a)
