'''
array of arrays
'''

def main():
	## variable size vector of vectors,
	## None is allowed as a sub-vector because each sub-vector is wrapped by std::shared_ptr
	arr = [][]int(
		(1,2,3),
		(4,5,6,7,8),
		None,
		#(x*x for x in range(4)),  ## TODO fix listcomps
		(x for x in range(20)),
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

	print('sub 3 items:')
	for i in arr[3]:
		print(i)

	print('sub 3 items changed:')
	arr[3][0] = 1000
	arr[3][1] = 1001
	arr[3][2] = 1002
	arr[3][3] = 1003
	for i in arr[3]:
		print(i)
