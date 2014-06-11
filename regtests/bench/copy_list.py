'''copy list micro benchmark'''

from time import time

def main():
	if PYTHON=='PYTHONJS':
		pythonjs.configure( direct_operator='+' )
		pythonjs.configure( direct_keys=True )
		pass

	a = list(range(1000))
	times = []
	for i in range(4):
		t0 = time()
		res = copy_list(a, 10000)
		tk = time()
		times.append(tk - t0)
	avg = sum(times) / len(times)
	print(avg)

def copy_list( a, n ):
	x = []
	for i in range(n):
		b = a[:]
		for j in range(10):
			b.append( j )
		x.append( b )
	return x

