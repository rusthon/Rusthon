"""inline dynamic object data"""
class A:
	def __init__(self):
		self.myattr = 22/7.0

def main():
	def my_wrapper(a,b, x,y,z,w):

		@returns( array=[32,32] )
		@gpu.main
		def gpufunc(x,y,z,w):
			float x
			float y
			float z
			float w
			float D = a.myattr
			vec4 V = vec4( x+D, y+D,z,w)
			return x+y+z+w+D

		return gpufunc(x,y,z,w)

	ai = A()
	bi = A()
	res = my_wrapper(ai,bi, 0.1, 0.2, 0.3, 0.4)
	print(res)
