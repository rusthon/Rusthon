Embed CPython Script
-------------

@embed
```python

class A():
	def pymethod(self):
		print 'hello world'

def foo():
	print 'foo'
	return A()

```

Build Options
-------------
* @link:python2.7
* @include:/usr/include/python2.7
```rusthon
#backend:c++
import Python.h
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