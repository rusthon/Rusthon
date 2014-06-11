"""list slice"""

class XXX:
	def __init__(self):
		self.v = range(10)
	def method(self, a):
		return a

def main():
	a = range(10)[:-5]
	TestError( len(a)==5 )
	TestError( a[4]==4 )

	#if BACKEND=='DART':
	#	print(a[...])
	#else:
	#	print(a)


	b = range(10)[::2]
	TestError( len(b)==5 )
	TestError( b[0]==0 )
	TestError( b[1]==2 )
	TestError( b[2]==4 )
	TestError( b[3]==6 )
	TestError( b[4]==8 )

	#if BACKEND=='DART':
	#	print(b[...])
	#else:
	#	print(b)


	c = range(20)
	d = c[ len(b) : ]

	#if BACKEND=='DART':
	#	print(d[...])
	#else:
	#	print(d)

	TestError( len(d)==15 )

	x = XXX()
	e = x.v[ len(b) : ]
	TestError( len(e)==5 )

	f = x.method( x.v[len(b):] )
	TestError( len(f)==5 )
