Embed CPython Script
-------------

The script below is marked with `@embed` which turns it into a static string in the final C++,
and is run after `cpython.initalize()` is called.


@embed
```python

class A():
	def __init__(self):
		self.value = 100
	def pymethod(self):
		print 'hello world'

def foo():
	print 'foo'
	return A()

```
CPython CAPI
------------
The code below shows how to use the `cpython` module that wraps around the CPython C-API.
https://docs.python.org/2/c-api/object.html

Build Options
-------------
* @link:python2.7
* @include:/usr/include/python2.7
```rusthon
#backend:c++
import cpython

def main():
	cpython.initalize()
	a = cpython.foo()
	print a
	print a.value
	a.pymethod()
	cpython.finalize()

```