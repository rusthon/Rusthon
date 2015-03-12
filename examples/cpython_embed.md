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
	a = cpython.foo()
	print a
	cpython.finalize()

```