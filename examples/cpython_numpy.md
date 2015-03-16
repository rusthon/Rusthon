Numpy Test
-------------

The Python script below is embedded in the final c++ exe, and run when `cpython.initalize` is called.
The `Mat` class can then be used from Rusthon using the special `->` syntax, that generates the required CPython C-API calls.

@embed
```python
import numpy

class Mat():
	def __init__(self):
		self.lst = []
		self.v1  = numpy.array([1,2,3,4]).astype(int)
		self.v2  = numpy.array([0.01,0.002,0.0003,0.000004,0.00005,6.1]).astype(float)
	def show(self):
		print 'self.lst:', self.lst
		print 'self.v1:', self.v1
		print 'self.v2:', self.v2

```

Below, example loops over numpy arrays: `v1` and `v2`, copies items from `v1` to `vec` a c++11 `std::vector` and appends them to
`m->lst` which is a normal Python array above `self.lst`.

Syntax for casting to Python Object types, `X as PYTYPE`, where PYTYPE can be:
* pyint
* pyi32
* pylong
* pyi64
* pyfloat
* pyf32
* pydouble
* pyf64
* pystring
* pybool


Build Options
-------------
* @link:python2.7
* @include:/usr/include/python2.7
```rusthon
#backend:c++
import cpython

def main():
	state = cpython.initalize()

	vec = []int()

	with gil:
		m = cpython.Mat()
		n1 = len(m->v1)
		n2 = len(m->v2)
		print 'length of vec1:', n1
		print 'length of vec2:', n2
		for i in range( len(m->v1) ):
			value = m->v1[i] as int
			print value
			vec.append(value)
			m->lst->append(i as pyint)
		m->show()
		for j in range( len(m->v2) ):
			a = m->v2[j] as float
			print a
			m->v2[j] = 3.14 as pyfloat
		m->show()

	print 'length of vec copy:', len(vec)

	cpython.finalize(state)

```