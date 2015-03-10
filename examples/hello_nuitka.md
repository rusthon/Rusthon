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

Rusthon
-------


```rusthon
#backend:c++
import nuitka

with pointers:
	def bar( pyob:PyObject ):
		#pyob.o_dict()
		method = PyObject_GetAttrString(pyob, cstr("pymethod"))
		print method

def main():
	pyob = nuitka.foo()
	bar( pyob )

```