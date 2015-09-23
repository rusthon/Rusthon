from runtime import *
"""variable keywords"""
class A:
	def __init__(self, **kw):
		a = 0
		for key in iter(kw):
			a += kw[key]
		self.value = a

def main():
	a = A(x=1,y=2)
	assert( a.value == 3 )
main()
