Nuitka
------

@nuitka
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
import cpython

with pointers:
	def bar( pyob:PyObject ):
		pyob->pymethod()

def main():
	s = cpython.initalize()
	with gil:
		pyob = cpython.foo()
		bar( pyob )
	cpython.finalize(s)

```