'''
returns array of arrays
'''

with pointers:
	def make_array() -> []int:
		arr = new([]int( 1,2,3,4 ))
		return arr

	def test_array( arr:[]int ):
		print( arr[0] )
		print( arr[1] )
		print( arr[2] )
		print( arr[3] )

	def main():
		a = make_array()
		print('arr length:', len(a))
		test_array(a)