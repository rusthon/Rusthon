'''@gpu class three.js'''
import three

three.Vector3.prototype.__struct_name__='ThreeVec3'

@gpu.object
class MyObject:
	@gpu.method
	float def mymethod(self, s):
		float s
		return (self.vec.x + self.vec.y + self.vec.z) * s

	def __init__(self, x,y,z):
		self.vec = new( three.Vector3(x,y,z) )



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
