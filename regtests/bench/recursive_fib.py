'''
Fibonacci Sequence
'''

from time import clock

def main():
	if PYTHON=='PYTHONJS':  ## about 25% faster with normal and javascript backends
		pythonjs.configure( direct_operator='+' )
		pass
		
	start = clock()
	a = F( 32 )
	print(clock()-start)


def F(n):
	if n == 0: return 0
	elif n == 1: return 1
	else: return F(n-1)+F(n-2)

