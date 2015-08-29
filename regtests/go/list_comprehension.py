'''
go list comprehensions
'''

class A:
	def __init__(self, x:int,arr:[]int):
		## note: names of args should match names on struct
		self.x = x
		self.arr = arr
		## TODO FIXME: allow arg names to be different from internal struct names
		#let self.arr : []int  = y

	def get(self) ->int:
		return self.arr[3] + self.x


def F( arr:[]int ):
	arr.append( 3 )

def main():
	a = []int(x for x in range(3))
	print a
	F( a )
	assert len(a)==4
	assert a[0]==0
	assert a[1]==1
	assert a[2]==2
	assert a[3]==3

	b = []A( 
		A(i,a) for i in range(2) 
	)
	assert b[1].get()==4
	print b
