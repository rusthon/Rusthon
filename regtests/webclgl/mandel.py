"""mandelbrot"""

def pprint(arr, w):
	x = []
	for a in arr:
		x.append(a)
		if len(x) >= w:
			print( [ round(y,2) for y in x] )
			x = []

def main():

	#@gpu.returns( array=[32,32], vec4=[4,4] )  ## TODO support dual return
	@returns( array=[32,32] )
	@gpu.main
	def gpufunc():

		vec2 c = get_global_id()
		#float cx = 0.5
		#float cy = 0.5

		float hue;
		float saturation;
		float value;
		float hueRound;
		int hueIndex;
		float f;
		float p;
		float q;
		float t;


		float x = 0.0;
		float y = 0.0;
		float tempX = 0.0;
		int i = 0;
		int runaway = 0;
		for i in range(100):
			tempX = x * x - y * y + float(c.x);
			y = 2.0 * x * y + float(c.y);
			x = tempX;
			if runaway == 0 and x * x + y * y > 100.0:
				runaway = i;

		return float(runaway) * 0.01

	w = 32
	h = 32

	#A = [w,h]

	res = gpufunc()
	pprint(res, w)

