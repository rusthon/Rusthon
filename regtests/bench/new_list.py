'''new list micro benchmark'''

from time import time

def main():
	if PYTHON=='PYTHONJS':
		pythonjs.configure( direct_operator='+' )
		pythonjs.configure( direct_keys=True )
		pass

	times = []
	a = []
	for i in range(10):
		t0 = time()
		for j in range(100000):
			b = [1,2,3,4,5,6,7,8,9]
			a.append( b )
		tk = time()
		times.append(tk - t0)
	avg = sum(times) / len(times)
	print(avg)


