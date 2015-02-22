'''
array of arrays objects
'''

class A:
	def __init__(self, id:int):
		self.id = id

	def method(self):
		print(self.id)

def main():
	a1 = A(1)
	a2 = A(2)
	a3 = A(3)

	arr = [][]A(
		(a1,a2,a3, A(4)),
		(a1,None),
		None,
	)
	print('length of array: ', len(arr))
	print( 'len subarray 0:  ', len(arr[0]) )
	print( 'len subarray 1:  ', len(arr[1]) )
	print('subarray 2 is nullptr:  ',arr[2] )
	print('subarray 0 ptr addr: ', arr[0])

	arr[0][2].method()