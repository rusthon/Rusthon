GPU Translation
---------------
A subset of Python with extra type information can be translated into a GLSL fragment shader.  The `@gpu` decorator marks a function for translation to GLSL.  All variables inside the function must be typed using GLSL types.  You can type your variables using decorators or special PythonJS type syntax.

Python GPU Subset:
-----------------

	. for loops `for i in range(n):`
	. if/elif/else
	. subroutines
	. input/output 1D/2D arrays of floats and or vec4
	. all variables must be given a GLSL typedef.

GLSL Types:
----------

	. int
	. float, float*
	. vec2, vec3, vec4

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


Typing with PythonJS C-style type prefixes
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

@typedef
--------
This decorator allows you to give a GLSL type to each variable in the function.  The syntax is `@typedef( VARIABLE_NAME=GLSL_TYPE )`.


get_global_id()
--------------
The GLSL function `get_global_id()` is part of the WebCLGL API and returns a vec2 that contains the current `x` and `y` index.

subroutines
-----------
Function subroutines are decorated with `@gpu`.  The main entry point function is decorated with `@gpu.main`. Example:

```
	@returns( float )
	@typedef( x=float, y=float )
	@gpu
	def mysub(x,y):
		return x-y

	@returns( array=[64,64] )
	@gpu.main
	def myfunc():
		return mysub( 1.1, 2.2 )

```

using arrays as arguments to gpu.main
---------------------------------------
You can pass a list of floats as arguments to your gpu entry point function, these will be translated into WebCLGL buffers and uploaded to the GPU.  By default the input arrays are expected to have a range of 0.0-1.0.  If you are using arrays with values outside of the default range, it can be changed by setting the `scale` variable on the list before passing it to the gpu entry point function, the scale integer sets the range from -scale to +scale.  Example:

```
@gpu.main
def gpufunc(a,b,c):
	float* a
	float* b
	float* c

A = [2.0 for i in range(64)]
A.scale=2
B = [-4.0 for i in range(64)]
B.scale=4
C = [1.5 for i in range(64)]
A.scale=2  ## set scale to largest integer

gpufunc( A, B, C )

```