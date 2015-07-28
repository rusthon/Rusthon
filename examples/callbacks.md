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


```

Main Source
-----------
Interfacing with external C libraries requires you declare the function type, and link the library.
The example above with hand written inlined C code is built with the final executeable.

syntax - `func()()`
------------
External C functions are typed as `func(args)(returns)`.


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


def mycb1() ->float:
	print 'callback1 returns float'
	return 100.1
def mycb2():
	print 'callback2 returns nothing'
	print 'OK'

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


def main():
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


	print 'testing calling c function with callback'
	t = call_callback1( mycb1 )
	print t

	call_callback2( mycb2 )

	print 'callback test ok'

```