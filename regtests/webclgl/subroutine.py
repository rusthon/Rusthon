"""subroutine"""

def main():
	with glsl as myfunc:
		def main(buffA, buffB, num):
			float* buffA
			float* buffB
			float num
			vec2 n = get_global_id()  ## WebCL API
			float result = 0.0
			for i in range(1000):
				result = sqrt(result + A[n] + B[n] + float(i))
			return mysub( result * num )

		float def mysub(x,y):
			float x
			float y
			return x+y

	A = [1,2,3]
	B = [4,5,6]
	res = myfunc( A, B, 2.0 )
	print(res)