"""while loop"""


def main():

	@returns( vec4=[2,32] )
	@gpu.main
	def gpufunc(x,y,z,w):
		float x
		float y
		float z
		float w
		vec4 V = vec4(x,y,z,w)
		return V

	res = gpufunc( 0.1, 0.2, 0.3, 0.4 )
	print(res)
