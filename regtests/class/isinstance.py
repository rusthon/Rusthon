from runtime import *
'''
builtin isinstance
'''
class A():
	pass

class B:
	pass

def main():
	print 'testing isinstance'
	a = A()
	b = B()
	assert( isinstance(a,A)==True )
	assert( isinstance(a,B)==False )
	assert( isinstance(a,dict)==False )

	assert( isinstance(b,B)==True )
	assert( isinstance(b,A)==False )

	c = [1,2]
	assert( isinstance(c, list)==True )
	assert( isinstance(c, dict)==False )
	assert( isinstance(c, A)==False )

	d = {'a':1, 'b':2}
	assert( isinstance(d, dict)==True )
	assert( isinstance(d, A)==False )

	print 'ok'

main()
