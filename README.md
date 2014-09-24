Introduction
------------
Gython is a transpiler written in Python that converts a python like language into Go.

[Syntax Documentation](https://github.com/PythonJS/PythonJS/blob/master/doc/go_syntax.md)


Installing
===============


gython.py
--------------------------------------
Install Python2.7 and git clone this repo, in the toplevel is the build script `gython.py`.  
Running gython.py from the command line and passing it one or more python scripts outputs
the Go translation to stdout.

Usage::

	gython.py file.py

Example::

	git clone https://github.com/gython/Gython.git
	cd Gython
	./gython.py myscript.py > myscript.go


Getting Started
===============
Gython supports classes and multiple inheritance, with method overrides and calling the parent class methods.

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

		def foo(self) -> int:
			a = A.foo(self)
			a += 100
			return a

```

Gython supports Go's typed maps.

```
	a = map[string]int{
		'x': 1,
		'y': 2,
		'z': 3,
	}

```

Gython supports array and map comprehensions.
Below is an array of integers, and a map of strings with integer keys.

```
	a = []int(x for x in range(3))
	b = map[int]string{ i:'xxx' for i in range(10) }
```

Gython supports Go's send data to channel syntax

```
	a = go.channel( int )
	a <- 1

```



Array and maps are always passed as pointers in a function call, this way the called function can modify the array or map inplace.
In the example below `a` is typed as an array of integers `[]int`, but it is actually retyped when transformed into Go as `*[]int`
```
def myfunc( a:[]int ):
	a.append( 100 )

x = []int()
myfunc( x )

```

Simple Generator Functions
==========================
Gython supports generator functions with a single for loop that yields from its main body.
The generator function can also yield once before the loop, and once after.
```
def fib(n:int) -> int:
	int a = 0
	int b = 1
	int c = 0
	for x in range(n):
		yield a
		c = b
		b = a+b
		a = c
	yield -1

def main():
	arr = []int()
	for n in fib(20):
		arr.append( n )
```

Generic High Order Functions
==========================
Gython supports generic functions, where the first argument can be an instance of different subclasses.
All the subclasses must share the same common base class.  In the function definition the first argument
is typed with the name of the common base class.  In the function below `my_generic`, the first argument `g`
is typed with the common base class: `def my_generic( a:A )`


```
class A:
	def __init__(self, x:int):
		int self.x = x

	def method1(self) -> int:
		return self.x

class B(A):

	def method1(self) ->int:
		return self.x * 2

class C(A):

	def method1(self) ->int:
		return self.x + 200


def my_generic( g:A ) ->int:
	return g.method1()

def main():
	a = A( 100 )
	b = B( 100 )
	c = C( 100 )

	x = my_generic( a )
	a.x == x

	y = my_generic( b )
	y==200

	z = my_generic( c )
	z==300

```