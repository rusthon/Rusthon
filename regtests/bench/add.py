'''
loop and add (integer)
'''

from time import clock

def main():
	start = clock()
	a = 0
	for i in range(1000000):
		a = 1 + 2
	print(clock()-start)
