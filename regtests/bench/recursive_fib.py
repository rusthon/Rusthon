'''
Fibonacci Sequence
'''

from time import clock

def F(n):
	if n == 0: return 0
	elif n == 1: return 1
	else: return F(n-1)+F(n-2)

def main():
	start = clock()
	a = F( 32 )
	print(clock()-start)
