"""dict tuple key"""


def main():
	s = ("1", "2", "3")
	a = (1,2,3)
	b = (1,2,3)
	c = ( a, b, 'XXX' )
	d = ('1', 2, 3)

	D = { d:100, s: 11, a: 22, c:44 }
	TestError( D[ d ] == 100)  ## this fails in both python and javascript mode
	TestError( D[ s ] == 11)   ## this fails in javascript mode
	TestError( D[ a ] == 22)
	TestError( D[ b ] == 22)
	TestError( D[ c ] == 44)
