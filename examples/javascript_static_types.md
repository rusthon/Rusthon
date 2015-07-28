JavaScript Backend - Static Types
-------

Enables runtime static type checking.

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

class B:
	def bar( self, x:A ):
		print 'bar'
		print x

	def test_array_of_A( self, x:[]A ):
		print 'B.test_array_of_A...'
		for item in x:
			print item


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

test()

```