class G:
	def method(self):
		print 'calling G.method'
		print 'hi'

class H( G ):
	def method(self):
		print 'calling H.method'
		print 'world'

class A:
	def __init__(self, a:G):
		print 'A.__init__'
		print(a)
		self.x = a

	def call(self):
		print 'A.call'
		self.f( self.x )

	def f(self, a:G):
		print 'A.f'
		print(a)


class B( A ):
	def f(self, g:G):
		print 'B.f'
		g.method()



def main():
	g = G()
	h = H()
	b1 = B( g )
	b2 = B( h )

	print('----------test1 b1 (g)')
	b1.call()
	print('----------test2 b2 (h)')
	b2.call()