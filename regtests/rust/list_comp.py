'''
rust list comprehensions
'''
class A:
	def __init__(self, id:int ):
		self.id = id


def test_pass_array( arr:[]int ):
	arr.append( 3 )

# `[]A` for c++11 backend becomes `std::shared_ptr<std::vector<std::shared_ptr<A>>>`
def test_pass_array_of_objects( arr:[]A, id:int ):
	a = A( id )
	arr.append( a )

def main():
	a = []int(x for x in range(3))
	assert len(a)==3
	assert a[0]==0
	assert a[1]==1
	assert a[2]==2

	test_pass_array( a )
	assert len(a)==4
	assert a[3]==3

	#b = []A( A(x) for x in ['list', 'comp'])  ## TODO fix me, infer type

	#stuff = []string('list', 'comp')
	#b = []A( A(x) for x in stuff)
	#b = []A( A(x) for x in ('list', 'comp'))  ## TODO fix strings

	b = []A( A(x) for x in (1,2,3,4))
	assert len(b)==4
	test_pass_array_of_objects( b, 5 )
	assert len(b)==5
