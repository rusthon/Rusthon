'''
returns array of arrays
'''
def make_array() -> [][]int:
	arr = [][]int(
		(1,2,3),
		(4,5,6,7,8)
	)
	return arr

def main():
	a = make_array()
	print( len(a))
	print( len(a[0]) )
	print( len(a[1]) )
