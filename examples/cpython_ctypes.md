ctypes test
-------------

note: `ctypes.CDLL('')` loads from the current process address space,
TODO what is the C name of C++ `hello_world`? even when defined with extern,
which makes the function compatible, it fails to be exported here,
or at least ctypes is unable to reach it using `ctypes.CDLL('')`

@embed
```python
import ctypes

def run_test():
	print 'cpython: running test...'
	lib = ctypes.CDLL('')
	print 'ctypes lib', lib
	#lib.hello_world()
	if not hasattr(lib, 'hello_world'):
		print 'hello_world C function missing'
	hw = getattr(lib, 'hello_world')  ## crashes here
	print hw
	#hw.restype = ctypes..
	#hw.argtypes = tuple(...)
	print 'test OK'

```

Build Options
-------------
* @link:python2.7
* @include:/usr/include/python2.7
```rusthon
#backend:c++
import cpython

with extern():
	def hello_world():
		print 'hello world'

def main():
	state = cpython.initalize()

	with gil:
		cpython.run_test()

	cpython.finalize(state)

```