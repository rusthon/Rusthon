'''
loop and add (integer)
'''

from time import clock

class A:
	def __init__(self, x:int,y:int,z:int):
		self.x = x; self.y = y; self.z = z
	def add(self, other:A) ->A:
		a = A(self.x+other.x, self.y+other.y, self.z+other.z)
		return a


def f2(y:int, a:A, b:A, c:A) ->int:
	s = 0
	for j in range(y):
		x = A(1,1,1)
		w = a.add(x).add(b).add(c)
		s += w.x - w.y
	return s

def f1( x:int, y:int, a:A, b:A, c:A ):
	for i in range(x):
		f2(y, a,b,c)

def main():
	if PYTHON=='PYTHONJS':  ## about 25% faster with normal and javascript backends
		pythonjs.configure( direct_operator='+' )
		pass

	#xsteps = 100000
	xsteps = 1000
	ysteps = 100

	start = clock()
	n = -1000000
	a = A(n,n+1,n)
	b = A(n,n+2,n)
	c = A(n,n+3,n)

	f1(xsteps, ysteps, a,b,c)
	print(clock()-start)

	# in Go a variable must be used for something, or the compiler will throw an error,
	# here just print 'a' to pass the benchmark.
	#print('#', a)
