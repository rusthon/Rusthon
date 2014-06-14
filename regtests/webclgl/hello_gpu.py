"""gpu test"""

def main():
	with glsl:
		def main(buffA, buffB, num):
			float* buffA
			float* buffB
			float num
			vec2 n = get_global_id()
			float result = 0.0
			for i in range(1000):
				result = sqrt(result + A[n] + B[n] + float(i))
			#out_float = result  ## translator should take care of this?
			return result