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

Gython supports list comprehensions.
Below is an array of integers.

```
	a = []int(x for x in range(3))
```

Gython supports Go's send data to channel syntax

```
	a = go.channel( int )
	a <- 1

```

Gython supports Go's typed maps.

```
	a = map[string]int{
		'x': 1,
		'y': 2,
		'z': 3,
	}

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