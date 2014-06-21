"""mandelbrot pure python"""

def pprint(arr, w):
	x = []
	for a in arr:
		x.append(a)
		if len(x) >= w:
			print( [ round(y,2) for y in x] )
			x = []

def main():

	@returns( array=[64,64] )
	@typedef( x=float, y=float, tempX=float, i=int, runaway=int, c=vec2)
	@gpu.main
	def gpufunc():
		c = get_global_id()
		x = 0.0
		y = 0.0
		tempX = 0.0
		i = 0
		runaway = 0
		for i in range(100):
			tempX = x * x - y * y + float(c.x)
			y = 2.0 * x * y + float(c.y)
			x = tempX
			if runaway == 0 and x * x + y * y > 100.0:
				runaway = i

		return float(runaway) * 0.01

	res = gpufunc()
	print(res)
	TestError( len(res)==64*64 )

	#pprint(res, 32)
	#for row in res:
	#	a = [ round(v,3) for v in row ]
	#	print( a )
