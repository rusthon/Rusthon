GPU Translation
---------------
A subset of Python with extra type information can be translated into a WebGL GLSL fragment shader.  
The shader program takes input in two ways: as arguments to the `main` function, argument types can be: int, float, or 1D and 2D arrays of floats or vec4.  This is the most efficient way to load large arrays into the shader.  The shader can also use input by inlining objects from the current javascript scope.

micro language:
-----------------

	. GLSL standard types
	. basic math ops and logic: if, elif, else, for i in range(n)
	. list of lists iteration with dynamic size
	. iterate over list of structs (dicts)
	. simple classes

	. define GPU `main` function with input arguments and subroutines
		. `gpu.main` can take arguments typed as: int, float, and float*
		. `gpu.main` returns a list of floats or vec4s

	. stream input variables into shader from attributes or method calls:
		. attribute: `float gpu_variable = self.cpu_variable`
		. method call: `float a = self.my_method( a,b,c, x=y,z=w )`
		. slice list: `float* a = self.mylist[n:]`



gpu.main
----------------------

The `@gpu.main` decorator marks a function as the entry point.  The main function requires the `@returns` decorator to set the return type to array or vec4, and return length (n) or 2D dimensions ([x,y]).  The example below would return 512x512 array of 1.1.


```
	@returns( array=[512,512] )
	@typedef( x=float, y=float )
	@gpu.main
	def gpu_func():
		x = 0.5
		y = 0.6
		return x+y

```

output index array index
----------------------

To get the index of the current fragment (index in the output array),
WebCLGL provides the function `get_global_id()` that returns a `vec2`.
The `x` and `y` attributes of the vec2 provide the 2D index.


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


subroutines
-----------
Function subroutines are decorated with `@gpu`

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

note: instead of using the @returns decorator, the return type of the `mysub` could also be placed at the start of the function def.

```
	@gpu
	float def mysub(x,y):
		float x
		float y
		return x-y

```

using arrays as arguments to gpu.main
---------------------------------------
You can pass a list of floats as arguments to your gpu entry point function, these will be translated into WebCLGL buffers and uploaded to the GPU.  By default the input arrays are expected to have a range of 0.0-1.0.  If you are using arrays with values outside of the default range, it can be changed by setting the `scale` variable on the list before passing it to the gpu entry point function, the scale integer sets the range from -scale to +scale.
In the example below the scale of `A` is increased, and `B` is changed to a 2D array by setting its `dims` attribute to [x,y] dimensions.

```
@gpu.main
def gpufunc(a,b):
	float* a
	float* b

A = [2.0 for i in range(64)]
A.scale=2

B = [ [0.5 for j in range(8)] for i in range(16)]
B.dims = [8,16]

gpufunc( A, B )

```

dynamic input variables
----------

Attributes on variables from the current javascript scope can be dynamically inlined into the shader.
In the example below, within the shader code, the variables `self.width`, `self.height` and `self.step` exist in the javascript scope, each call to `run` recompiles the shader and copies the variable attributes into the shader.

```
class myclass:
	def __init__(self):
		self.width = 100
		self.height = 64
		self.step = 0.01

	def run(self, w, h, s):
		self.width = w
		self.height = h
		self.step = s

		@returns( array=[8,8] )
		@gpu.main
		def gpufunc():
			float b = 0.0
			for x in range( self.width ):
				for y in range( self.height ):
					b += self.step
			return b

		return gpufunc()

A = myclass()
A.run(4,4, 0.8)
A.run(16,16, 0.5)


```

float list
--------------

Lists are translated into float32 arrays.
Iteration over a list is allowed using this syntax: `for i in range(len(A)):`.  The values of and length of `A` can vary for each call.  The dynamic array is assigned to a local variable and typed as `float*`

A list can be sliced when it is assigned to a local variable, in the example below the first 4 items of `mylist` are trimed away.

```
class myclass:
	def __init__(self):
		self.mylist = [0.0 for i in range(64)]

	def run(self):
		@returns( array=[8,8] )
		@gpu.main
		def gpufunc():
			float b = 0.0
			float* A = self.mylist[4:]
			for i in range( len(A) ):
				b += A[i]
			return b

		return gpufunc()


```

int array
----------

Integer arrays are defined using the JavaScript type `Int16Array`.
note: GLSL 1.2 limits integers to 16bit precision.
[http://www.opengl.org/registry/doc/GLSLangSpec.Full.1.20.8.pdf](see GLSL 1.2 spec)

```
		self.intarray = new(Int16Array(n))
		self.intarray[0] = 100
		@returns( array=n )
		@gpu.main
		def gpufunc():
			int* A = self.intarray
			return float( A[0] )

```

float list of lists
---------------

Looping over an array of arrays requires an outer iterator loop `for sub in arr`,
and the inner loop iterate over the length of the first sub-array: `for i in range(len(arr[0]))`
All sub-arrays should have the same length, or at least as long as the first item `arr[0]`.
The number of arrays inside the main array, and the values/lengths of the sub-arrays, can vary each call.
Note: looping over many large arrays of arrays could be slow or cause the GLSL compiler to fail,
this happens because WebGLSL has no builtin support for array of arrays, and the generated code is large.

```
class myclass:
	def __init__(self):
		pass

	def run(self, w, h, length):
		self.array = [ [x*y*0.5 for y in range(h)] for x in range(w) ]

		@gpu.main
		def gpufunc():
			float* A = self.array
			float b = 0.0
			for subarray in A:
				for j in range( len(self.array[0]) ):
					b += subarray[j]
			return b


```

list of dicts
---------------
Use the for-iter loop to iterate over a list of dicts `for s in iter(A):`
Regular JavaScript objects and Python dicts are uploaded to the shader as GLSL structs.
The struct type name and GLSL code are generated at runtime based on the contents of
each dict.  A struct may contain: ints, floats and array of floats attributes.
To use an integer value wrap it in a Int16Array with a single item,
or call `int16(n)` which takes care of that for you.

```
class myclass:

	def new_struct(self, g):
		return {
			'attr1' : 0.6 + g,
			'attr2' : int16(g)
		}


	def run(self, w):
		self.array = [ self.new_struct( x ) for x in range(w) ]

		@returns( array=64 )
		@gpu.main
		def gpufunc():
			struct* A = self.array
			float b = 0.0
			for s in iter(A):
				b += s.attr1 + float(s.attr2)
			return b

		return gpufunc()

```

external method calls
---------------------
Methods on external objects can be called within the shader function.
This is useful for getting runtime data that is loop invariant.

```
class myclass:
	def __init__(self, i):
		self.index = i

	def get_index(self):
		return self.index

	def run(self, n):
		self.intarray = new(Int16Array(n))
		self.intarray[ self.index ] = 99

		@returns( array=n )
		@gpu.main
		def gpufunc():
			int* A = self.intarray
			return float( A[self.get_index()] )

		return gpufunc()

def main():
	m = myclass(10)
	r = m.run(64)

```

user defined classes
-------
A class decorated with `@gpu.object` will have its methods marked with `@gpu.method` translated into shader code.  GPU methods must be defined in use order, a method is defined before it is used by another method.  Recursive calls are not allowed.


```
@gpu.object
class MyObject:
	@gpu.method
	float def subroutine(self, x,y):
		float x
		float y
		return x + y * self.attr2

	@gpu.method
	float def mymethod(self, x,y):
		float x
		float y
		if self.index == 0:
			return -20.5
		elif self.index == 0:
			return 0.6
		else:
			return self.subroutine(x,y) * self.attr1

	def __init__(self, a, b, i):
		self.attr1 = a
		self.attr2 = b
		self.index = int16(i)


class myclass:
	def run(self, w):
		self.array = [ MyObject( 1.1, 1.2, x ) for x in range(w) ]

		@returns( array=64 )
		@gpu.main
		def gpufunc():
			struct* A = self.array
			float b = 0.0

			for s in iter(A):
				b += s.mymethod(1.1, 2.2)

			return b

		return gpufunc()

```

external type conversion
------------------------
@gpu.object classes can also contain sub-structures and GLSL types: `vec3`.
To define a sub structure call the `gpu.object(class, name)` function.
The example below types THREE.js Vector3 as a GLSL `vec` type.

```
import three
gpu.object( three.Vector3, 'vec3' )

```

Then when a `three.Vector3` is assigned to an attribute in the __init__ function of the @gpu.object
class it will be inlined into the shader as a `vec3`.

```
@gpu.object
class MyObject:
	def __init__(self, x,y,z, a,b,c):
		self.vec1 = new( three.Vector3(x,y,z) )
		self.vec2 = new( three.Vector3(a,b,c) )

	@gpu.method
	float def mymethod(self):
		return self.vec1.x + self.vec2.y

```

array of mat4 input and output
------------------------------

The gpu.main function may also return `mat4`, an array of 4x4 float32 matrices, by using a `-> mat4` function return annotation. In this case the wrapper function will contain an attribute `return_matrices`,
appending Float32Array buffers to this list will update their values when the wrapper is called.

Within the shader you can get the current index of the matrix in `return_matrices` with ellipsis on an iterable.
Below `A[...]` gets the current index in `gpufunc.return_matrices`.

```
class myclass:
	def run(self, w):
		self.array = [ MyObject( x+1.0 ) for x in range(w) ]

		@typedef(o=MyObject)
		@gpu.main
		def gpufunc() -> mat4:
			struct* A = self.array
			o = A[...]
			return o.mat

		for ob in self.array:
			gpufunc.return_matrices.append( ob.mat.elements )

		return gpufunc()

```