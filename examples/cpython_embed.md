Embed CPython Script
-------------

The script below is marked with `@embed` which turns it into a static string in the final C++,
and is run after `cpython.initalize()` is called.


@embed
```python

class A():
	def pymethod(self):
		print 'hello world'

def foo():
	print 'foo'
	return A()

```
CPython CAPI
------------
example shows how to use the fake `cpython` module, and directly use the CPython C-API.
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
	pyfoo = cpython.foo()
	a = PyObject_Call(pyfoo, inline('Py_BuildValue("()")'), None)
	pymeth = PyObject_GetAttrString(a, cstr("pymethod"));
	PyObject_Call(pymeth, inline('Py_BuildValue("()")'), None)
	print a

	cpython.finalize()

```