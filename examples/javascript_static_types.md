JavaScript Backend - Static Types
-------

By adding static types to function arguments and its return type,
this enables runtime static type checking, and when an invalid type is found,
`TypeError` is raised.  This adds safety and helps in debugging your code,
but has some runtime performance overhead.  Once you have tested and your program
runs without errors, you can do the final compile using the option `--release`, example:

```bash
rusthon.py myinput.md --release myoutput.tar
```


To run this example, install nodejs, and run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_static_types.md --run=myapp.js
```


Example
--------

notes:
* the `float` type is true for any number, because `0.0` becomes `0`
* strings can be typed with `str` or `string`

@myapp.js
```rusthon
#backend:javascript
from runtime import *

class A:
	def foo( self, x:B ):
		print 'foo'
		print x

	def test_int( self, x:int ):
		print x

	def test_float( self, x:float ):
		print x

	def test_string( self, x:string):
		print x

	def test_int32array( self, x:Int32Array):
		print x

	def test_intarray(self, x:[]int):
		for item in x:
			print item

class B:
	def bar( self, x:A ):
		print 'bar'
		print x

	def test_array_of_A( self, x:[]A ):
		print 'B.test_array_of_A...'
		for item in x:
			print item

	def test_2D_array_of_A( self, x:[][]A ):
		print 'B.test_array_of_A...'
		for item in x:
			print item

	def test_callback( self, x:Function ):
		return x(1,2)

	def test_callback_typed( self, x:func(int float string)(float) ):
		return x(1,2, 'callback typed OK')


def test():
	a = A()
	b = B()
	a.foo( b )
	#a.foo( 1 )  ## not allowed, throw error
	b.bar( a )

	a.test_int( 1 )
	a.test_float( 1.1 )
	a.test_string('hello world')
	#a.test_string(1)  ## not allowed

	arr = new Int32Array([1,2,3,4])
	a.test_int32array( arr )

	a.hello = 'world'
	#arra = [b,a,a,a,a]  ## not allowed, note only check first element
	arra = [a,a,a,a]
	b.test_array_of_A( arra )

	b.test_2D_array_of_A(
		[arra, arra, arra]
	)

	def f(x,y):
		return x+y

	assert b.test_callback( f )

	def ftyped(x:int, y:float, z:string) -> float:
		print z
		return x+y

	assert b.test_callback_typed( ftyped )

	def ftyped_invalid1(x:float, y:float):
		return x+y

	def ftyped_invalid2(x:int, y:float, z:string):
		print x+y

	try:
		b.test_callback_typed( ftyped_invalid1 )  ## this fails properly
	except TypeError:
		print 'caught TypeError OK'

	## these also fail properly ##
	#b.test_callback_typed( ftyped_invalid2 )
	#b.test_callback_typed( 1 )


test()

```