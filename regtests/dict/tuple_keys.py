"""dict tuple key"""

class A: pass
class B:
	def __init__(self):
		pass

def main():
	s = ("1", "2", "3")
	a = (1,2,3)
	b = (1,2,3)
	c = ( a, b, 'XXX' )
	d = ('1', 2, 3)

	D = { d:100, s: 11, a: 22, c:44 }
	TestError( D[ d ] == 100)
	TestError( D[ s ] == 11)
	TestError( D[ a ] == 22)
	TestError( D[ b ] == 22)
	TestError( D[ c ] == 44)

	aa = A()
	bb = B()
	ab = ( A(), B() )
	D2 = { aa: 'hello', bb: 'world', ab:'XXX' }
	TestError( D2[aa]=='hello' )
	TestError( D2[bb]=='world' )
	TestError( D2[ab]=='XXX')

	r = { s:1, a:aa }
	r2 = {}
	for x in [ s, a ]:
		r2[ x ] = r[ x ]
	TestError( r[s] is r2[s] )