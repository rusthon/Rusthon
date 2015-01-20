'''
array of arrays
'''

def main():
	arr = [][]int(
		(1,2,3),
		(4,5,6,7,8),
		None,
		#(x*x for x in range(4)),
	)
	print( len(arr))
	print( len(arr[0]) )
	print( len(arr[1]) )
	if arr[2] is None:
		print('nullptr works ok!')
	else:
		print('never reached')

	print('sub 0 items:')
	for i in arr[0]:
		print( i )

	print('sub 1 items:')
	sub = arr[1]
	for i in sub:
		print(i)