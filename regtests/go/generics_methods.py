class G:
	def method(self):
		print 'hi'

class H( G ):
	def method(self):
		print 'world'

class A:
	def __init__(self, a:G):
		self.x = a

	def call(self):
		self.f( self.x )

	def f(self, a:G):
		print(a)


class B( A ):
	def f(self, g:G):
		g.method()



def main():
	g = G()
	h = H()
	b1 = B( g )
	b2 = B( h )

	b1.call()
	b2.call()