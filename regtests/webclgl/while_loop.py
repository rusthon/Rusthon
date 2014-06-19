"""while loop"""


def main():

	@returns( array=[32,32] )
	@gpu.main
	def gpufunc():
		int i = 0
		while i < 10:
			i += 1
		return float(i) * 0.01

	res = gpufunc()
	for row in res:
		a = [ round(v,3) for v in row ]
		print( a )
