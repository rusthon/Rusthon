"""inline dynamic object data"""
class A:
	def __init__(self, value):
		self.readonly_attr = value

def main():
	def my_wrapper(a,b, x,y,z,w):

		@returns( array=[32,32] )
		@gpu.main
		def gpufunc(x,y,z,w):
			float x
			float y
			float z
			float w
			float D = a.readonly_attr
			vec4 V = vec4( x+D, y+b.readonly_attr,z,w)
			return V.x

		return gpufunc(x,y,z,w)

	ai = A(22/7.0)
	bi = A(0.420)
	res = my_wrapper(ai,bi, 0.1, 0.2, 0.3, 0.4)
	print(res)
