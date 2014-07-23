"""dict tuple key"""


def main():
	a = (1,2,3)
	b = (1,2,3)
	c = ( a, b, 'XXX' )

	D = { a: 22, c:44 }
	TestError( D[ a ] == 22)
	TestError( D[ b ] == 22)
	TestError( D[ c ] == 44)
