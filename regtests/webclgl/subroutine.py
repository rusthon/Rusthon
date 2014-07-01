"""subroutine"""

def main():
	@gpu
	float def mysub(x,y):
		float x
		float y
		return x-y

	@returns( array=64 )
	@gpu.main
	def myfunc(a):
		float* a
		vec2 id = get_global_id()
		return mysub( 1.1 * a[id], 2.2 )


	A = [1.3 for i in range(64)]
	res = myfunc( A )
	print(res)