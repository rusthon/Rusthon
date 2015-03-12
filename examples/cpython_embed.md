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
The code below shows how to use the `cpython` module and embed libpython directly using the CPython C-API.
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

	## old style - directly using C API ##
	#pyfoo = cpython.foo()
	#empty_tuple = Py_BuildValue(cstr("()"))
	#a = PyObject_Call(pyfoo, empty_tuple, None)
	#pymeth = PyObject_GetAttrString(a, cstr("pymethod"))
	#PyObject_Call(pymeth, empty_tuple, None)
	#v = PyInt_AS_LONG(
	#	PyObject_GetAttrString(a, cstr("value"))
	#)
	#print v


	cpython.finalize()

```