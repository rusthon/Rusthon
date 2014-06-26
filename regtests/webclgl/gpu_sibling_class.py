'''@gpu sibling class'''
import three

gpu.object( three.Vector3, 'vec3' )

@gpu.object
class Other:
	#@gpu.method
	def __init__(self, a, b):
		#vec3 a
		#vec3 b
		self.vecA = a
		self.vecB = b

	@gpu.method
	float def omethod(self, s):
		float s
		return (self.vecA.x + self.vecA.y + self.vecB.z) * s


@gpu.object
class MyObject:
	@typedef( ob=Other )
	@gpu.method
	float def mymethod(self, s):
		float s
		#o = Other( self.v1, self.v2 )
		#return o.omethod(s)
		return self.ob.omethod(s)

	def __init__(self, x,y,z):
		self.v1 = new( three.Vector3(x,y,z) )
		self.v2 = new( three.Vector3(x,y,z) )
		self.ob = Other(self.v1, self.v2)


class myclass:
	def run(self, w):
		self.array = [ MyObject( 1.1, 1.2, 1.3 ) for x in range(w) ]

		@returns( array=64 )
		@gpu.main
		def gpufunc():
			struct* A = self.array
			float b = 0.0

			for s in iter(A):
				b += s.mymethod(1.1)

			return b

		return gpufunc()

def main():
	m = myclass()
	r = m.run(8)
	print(r)
