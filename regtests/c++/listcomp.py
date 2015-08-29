'''
list comprehension
'''


def main():
	a = []int( x*2 for x in range(10) )
	print(len(a))
	for item in a:
		print(item)

	## TODO fix slice copy:
	## *** Error in `/tmp/listcomp': free(): invalid pointer: 0x000000000216d218 ***
	#b = [][]int( a[:] for i in range(4)	)
	#print(len(b))
	#print(b[0])
	#print(b[1])
	#print(b[2])
	#print(b[3])
