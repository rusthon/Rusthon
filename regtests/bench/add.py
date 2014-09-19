'''
loop and add (integer)
'''

from time import clock


def main():
	if PYTHON=='PYTHONJS':  ## about 25% faster with normal and javascript backends
		pythonjs.configure( direct_operator='+' )
		pass

	start = clock()
	a = -1000000
	for i in range(1000000):
		for j in range(100):
			a = 1 + 2
	print(clock()-start)

	# in Go a variable must be used for something, or the compiler will throw an error,
	# here just print 'a' to pass the benchmark.
	print('#', a)
