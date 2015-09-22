from runtime import *
"""variable keywords"""
class A:
	def f2(self, **kw):
		a = 0
		for key in kw.keys():
			a += kw[key]
		return a

def main():
	a = A()
	assert( a.f2(x=1,y=2) == 3 )
main()
