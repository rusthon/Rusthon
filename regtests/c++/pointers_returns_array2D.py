'''
returns array of arrays
'''

with pointers:
	def make_array() -> [][]int:
		arr = new(
			[][]int(
				(1,2,3),
				(4,5,6,7,8)
			)
		)
		return arr

	def test_array( arr:[][]int ):
		print( arr[0][0] )

	def main():
		a = make_array()
		print( len(a))
		print( len(a[0]) )
		print( len(a[1]) )

		test_array(a)