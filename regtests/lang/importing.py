from runtime import *

try:
	import mylib
except:
	print 'TODO import mylib'

## translates correctly to js, but is syntax error `import` unknown keyword in nodejs.
#from mylib import A,B,MyClass

#class Sub(mylib.MyClass):  ## TODO
class Sub:
	def foo(self, x):
		print 'foo'
		return x

def main():
	s = Sub()
	assert s.foo(10)==10

main()
