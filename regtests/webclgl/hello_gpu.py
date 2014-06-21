"""gpu test"""

def main():
	@returns( array=[4,16])
	@gpu.main
	def myfunc(a, b, num):
		float* a
		float* b
		float num
		vec2 n = get_global_id()  ## WebCL API
		float result = 0.0
		for i in range(1000):
			result = sqrt(result + a[n] + b[n] + float(i))
		return result * num

	A = [ 0.5 for x in range(64) ]
	B = [ 0.25 for x in range(64) ]
	res = myfunc( A, B, 0.1 )
	print(res)