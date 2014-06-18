GPU Translation
---------------
A subset of Python with extra type information can be translated into a GLSL fragment shader.  The `@gpu` decorator marks a function for translation to GLSL.  All variables inside the function must be typed using GLSL types.  You can type your variables using decorators or special PythonJS type syntax.

Typing with Decorators
----------------------

```
	@returns( array=[512,512] )
	@typedef( x=float, y=float, tempX=float, i=int, runaway=int, c=vec2)
	@gpu.main
	def gpu_mandelbrot():
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

```


Typing C-style
----------------------

```
	@returns( array=[512,512] )
	@gpu.main
	def gpu_mandelbrot():
		vec2 c = get_global_id()
		float x = 0.0
		float y = 0.0
		float tempX = 0.0
		int i = 0
		int runaway = 0
		for i in range(100):
			tempX = x * x - y * y + float(c.x)
			y = 2.0 * x * y + float(c.y)
			x = tempX
			if runaway == 0 and x * x + y * y > 100.0:
				runaway = i
		return float(runaway) * 0.01

```

@returns
---------
The main entry point function marked with `@gpu.main` must also use the `@returns(array=[w,h])` decorator to declare the width and height of the 2D array that it will return. Subroutines must also use the `@returns` decorator to declare their GLSL return type like this: `@returns(float)`


get_global_id()
--------------
The GLSL function `get_global_id()` is part of the WebCLGL API and returns a vec2 that contains the current `x` and `y` index.