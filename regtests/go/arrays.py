"""array types"""

def test_pass_array_as_arg( arr:[]int ):
	arr.append( 5 )

def main():
	a = []int(1,2,3)
	print a
	assert a[0]==1
	assert len(a)==3
	a.append( 4 )
	assert len(a)==4

	test_pass_array_as_arg( a )
	assert len(a)==5

	b = [2]int(100,200)
	assert b[0]==100
	assert b[1]==200

	#c = a[:2]
	#TestError( len(c)==2 )

	#d = range(10)
	#TestError(len(d)==10)
	#d.append(99)
	#TestError(len(d)==11)

	#e = range(2,10)
	#TestError(len(e)==8)

	#f = range(2,10, 2)
	#TestError(len(f)==4)
