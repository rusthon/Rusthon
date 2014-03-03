'''
builtin isinstance
'''
class A:
	pass

class B:
	pass

def main():
	a = A()
	b = B()
	TestError( isinstance(a,A)==True )
	TestError( isinstance(a,B)==False )
	TestError( isinstance(a,dict)==False )

	TestError( isinstance(b,B)==True )
	TestError( isinstance(b,A)==False )

	c = [1,2]
	TestError( isinstance(c, list)==True )
	TestError( isinstance(c, dict)==False )
	TestError( isinstance(c, A)==False )

	d = {'a':1, 'b':2}
	TestWarning( isinstance(d, dict)==True )  ## in javascript-mode this will fail
	TestError( isinstance(d, A)==False )
