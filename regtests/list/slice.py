from runtime import *
"""list slice"""

class XXX:
	def __init__(self):
		self.v = range(10)
	def method(self, a):
		return a

def main():
	a = range(10)[:-5]
	assert( len(a)==5 )
	assert( a[4]==4 )

	print '--------'
	b = range(10)[::2]
	print b
	assert( len(b)==5 )
	assert( b[0]==0 )
	assert( b[1]==2 )
	assert( b[2]==4 )
	assert( b[3]==6 )
	assert( b[4]==8 )

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

	assert( len(d)==15 )

	x = XXX()
	e = x.v[ len(b) : ]
	assert( len(e)==5 )

	f = x.method( x.v[len(b):] )
	assert( len(f)==5 )

main()
