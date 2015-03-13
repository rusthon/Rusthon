CPython Threads GIL Test
-------------


@embed
```python
import time

class A():
	def __init__(self):
		self.value = 0
	def run(self):
		print 'starting run'
		while i < 1000:
			self.value += 1
			time.sleep(0.01)
		print 'end run'

def make_A():
	return A()

```

note: `spawn` creates a c++11 thread.

Build Options
-------------
* @link:python2.7
* @include:/usr/include/python2.7
```rusthon
#backend:c++
import cpython


def thread1( input: chan PyObject, output: chan PyObject ):
	pyob = <- input  ## gets from main
	for i in range(10000):
		v = pyob->value as int
		print 'thread1:', v
		output <- pyob  ## sends to thread2

def thread2( C: chan PyObject):
	for i in range(10000):
		pyob = <- C
		v = pyob->value as int
		print 'thread2:', v


def main():
	cpython.initalize()

	input  = channel(PyObject)
	output = channel(PyObject)

	spawn(
		thread1(input, output)
	)
	spawn(
		thread2(output)
	)

	a = cpython.make_A()
	print 'addr of a:', a

	input <- a

	cpython.finalize()

```