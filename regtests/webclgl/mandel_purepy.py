"""mandelbrot pure python"""

def pprint(arr, w):
	x = []
	for a in arr:
		x.append(a)
		if len(x) >= w:
			print( [ round(y,2) for y in x] )
			x = []

def main():

	@returns( array=[32,32] )
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
	pprint(res, 32)

