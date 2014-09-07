PythonJS Go Syntax
===============

PythonJS supports a fully typed subset of Python with extra syntax to support the Golang backend.


select
-------
Below `A` and `B` are typed as `chan int`.  Data is read from a channel with `<-`.
```
	def select_loop(A:chan int, B:chan int):
		print('starting select loop')
		y = 0
		while True:
			select:
				case x = <- A:
					y += x
				case x = <- B:
					y += x

```

maps
-------
Go maps store key value pairs.  The key type is given first enclosed in brackets, the value type is given after.
The example below shows a map with string keys and integer values

```
	a = map[string]int{
		'x': 1,
		'y': 2,
		'z': 3,
	}
```

map iteration
-------------
The key value pairs can be looped over with a for loop.
```
	def main():
		a = map[string]int{'x':100, 'y':200}
		b = ''
		c = 0
		for key,value in a:
			b += key
			c += value
```

arrays
------
Go typed arrays are defined with an optional size followed by the type, and values passed as arguments to the constructor.
Items in an array can be iterated over with a normal `for x in a` loop.  Arrays also support index value pair loops using `enumerate`

```
	a = []int(1,2,3)
	b = [2]int(100,200)

```

classes
-------
A Python class is translated into a Go struct with methods.  Below a dict is used to type all the attribute variables that `self` will use.
```
	class A:
		{
			x:int,
			y:int,
			z:int,
		}
		def __init__(self, x:int, y:int, z:int=1):
			self.x = x
			self.y = y
			self.z = z


```

subclasses
----------
Subclasses can mix multiple classes, and override methods from the parent class.

```
	class A:
		def foo(self) -> int:
			return 1

	class B:
		def bar(self) -> int:
			return 2

	class C( A, B ):
		def call_foo_bar(self) -> int:
			a = self.foo()
			a += self.bar()
			return a

		## override foo ##
		def foo(self) -> int:
			return 100

	def main():
		a = A()
		b = B()

		c = C()

		## below is all true ##
		b.bar()==2
		c.bar()==2
		c.foo()==100
		c.call_foo_bar()==102

``` 

callbacks
---------
Functions and methods can be passed as callbacks to other functions.  The function argument type must contain the keyword `func` followed by the type signature of the callback (argument types) and (return type).  Below the method is typed as `func(int)(int)`

```
class A:
	{
		x:int,
		y:int,
		z:int,
	}
	def __init__(self, x:int, y:int, z:int=1):
		self.x = x
		self.y = y
		self.z = z

	def mymethod(self, m:int) -> int:
		return self.x * m

	def call_method( cb:func(int)(int), mx:int ) ->int:
		return cb(mx)

	def main():
		a = A( 100, 200, z=9999 )
		c = call_method( a.mymethod, 4 )
		print( c )

```

goroutines
----------
The function `go` can be called to spawn a new function call as a goroutine
```
	go( myfunc(x,y,z) )

```

channels
--------
To make a new Go channel call `go.channel(type)`, this is the same as in Go calling `make(chan type)`.
```
	c = go.channel(int)
```

list comprehensions
-------------------

```
	a = []int(x for x in range(3))
```