'''
loop and add (integer)
'''

from time import clock


def main():
	if PYTHON=='PYTHONJS':  ## about 25% faster with normal and javascript backends
		pythonjs.configure( direct_operator='+' )
		pass

	start = clock()
	a = 0
	for i in range(10000000):
		a = 1 + 2
	print(clock()-start)
