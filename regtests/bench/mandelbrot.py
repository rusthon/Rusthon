"""mandelbrot benchmark"""
from time import time

def pprint(arr, w):
	x = []
	for a in arr:
		x.append(a)
		if len(x) >= w:
			print( [ round(y,2) for y in x] )
			x = []

def mandelbrot_numpy(size=512, exit_limit=100):
	img_array = numpy.zeros([size, size], int) 
	for y in range(size):
		for x  in range(size): 
			c = complex(x / float(size) * 4 - 2,
						y / float(size) * 4 - 2)
			z = c
			for i in range(exit_limit):
				z = (z**2) + c
				img_array[y, x] += 1
				if abs(z) > 2:
					# z is escaping to infinity, so point is not in set
					break
			else:
				# if loop is exausted, point is inside the set
				img_array[y, x] = 0
	return img_array


def main():

	@returns( array=[512,512] )
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

	start = time()

	if PYTHON == 'PYTHONJS':
		res = gpufunc()
		#pprint(res, 32)
	else:
		res = mandelbrot_numpy()

	print(time()-start)
