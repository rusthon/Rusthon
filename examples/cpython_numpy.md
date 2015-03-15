Numpy Test
-------------


@embed
```python
import numpy

class Mat():
	def __init__(self):
		self.v1 = numpy.array([1,2,3,4]).astype(int)
		self.v2 = numpy.array([1,2,3,4,5,6]).astype(int)


```


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

	print 'length of vec copy:', len(vec)

	cpython.finalize(state)

```