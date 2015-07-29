Callback Functions/Methods
----------------

hand written C example, two callback types.
The C functions are redeclared below inside of `with extern(abi="C")`

```c

float call_callback1( float(*cb)(void) ) {
	return cb();
}

void call_callback2( void(*cb)(void) ) {
	cb();
}

void call_callback3( void(*cb)(float) ) {
	cb(101.1);
}
void call_callback4( void(*cb)(float,float) ) {
	cb(400.0, 20.0);
}


```

Main Source
-----------
Interfacing with external C libraries requires you declare the function type, and link the library.
The example above with hand written inlined C code is built with the final executeable.

syntax - `func()()`
------------
External C functions are typed as `func(args)(returns)`.

Note: the argument types given to `func` and `lambda` are not comma separated,
instead they are space separated, so they are not confused with the containing function argument list.
example: `func(int float)()` is a callback that takes two arguments, the first is an integer, and the second is a float.


syntax - `lambda()()`
------------

C++11 lambda functions are typed instead with `lambda(args)(returns)`.
This is required because C++11 lambda functions are different from standard C callback pointers.



```rusthon
#backend:c++

with extern(abi="C"):

	# cb takes no arguments and returns a float
	def call_callback1( cb:func()(float) ) -> float:
		pass

	# cb takes no arguments and returns nothing
	def call_callback2( cb:func()() ):
		pass

	# cb takes one and returns nothing
	def call_callback3( cb:func(float)() ):
		pass

	# cb takes two and returns nothing
	# note func args are space separated
	def call_callback4( cb:func(float float)() ):
		pass

def mycb1() ->float:
	print 'callback1 returns float'
	return 100.1
def mycb2():
	print 'callback2 returns nothing'
	print 'OK'
def mycb3(a:f32):
	print 'callback3 takes a float and returns nothing'
	print a
def mycb4(a:f32, b:f32):
	print 'callback4 takes two floats and returns nothing'
	print a+b

class Vec2:
	def __init__(self, x:f32=4.0, y:f32=0.2):
		self.x = x
		self.y = y

	def add(self, other:Vec2) ->Vec2:
		print 'ADD....'
		v = Vec2(self.x+other.x, self.y+other.y)
		return v

	def show(self):
		print self.x
		print self.y


def call_method( callback:lambda(Vec2)(Vec2), other:Vec2 ) ->Vec2:
	v = callback( other )
	return v

def test_c_callbacks():
	print 'testing calling c function with callback'
	t = call_callback1( mycb1 )
	print t

	call_callback2( mycb2 )

	call_callback3( mycb3 )
	call_callback4( mycb4 )


def main():
	test_c_callbacks()

	v1 = Vec2( 1.0, 2.0 )
	v2 = Vec2( 100.0, 200.0 )
	v1.show()
	v2.show()
	print 'callback test...'
	v3 = call_method(
		lambda o=Vec2: v1.add(o), 
		v2 
	)
	v3.show()
	print 'callback ok'
	v4 = Vec2(x=99.9)
	v4.show()

	## TODO - can not construct this way because at least one keyword argument is required.
	#v5 = Vec2(99.9)
	#v5.show()
	## TODO - this is valid python but is bad style
	#v5 = Vec2(420, y=-1000)
	#v5.show()

	print 'callback test ok'

```