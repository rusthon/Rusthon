'''
go list comprehensions
'''

class A:
	def __init__(self, x:int,y:[]int):
		int self.x = x
		[]int self.arr = y
	def get(self) ->int:
		return self.arr[3] + self.x


def F( arr:[]int ):
	arr.append( 3 )

def main():
	a = []int(x for x in range(3))
	F( a )
	TestError( len(a)==4 )
	TestError( a[0]==0 )
	TestError( a[1]==1 )
	TestError( a[2]==2 )
	TestError( a[3]==3 )

	b = []A( A(i,a) for i in range(2) )
	TestError( b[1].get()==4 )