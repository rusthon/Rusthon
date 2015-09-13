from runtime import *
"""Function call with the name of a parameter without default value"""
def f1(a):
	return a

def f2(a=1, b=2):
	return a + b

def main():
	print 'testing calling named parameters'
	assert f1(10)==10
	assert f2()  ==3
	assert f2(a=100) == 102
	assert f2(b=500) == 501

	## GOTCHA: calling a function that expects a named keyword parameter,
	## and not giving any named parameters is not valid in Rusthon.
	## this works in regular python, but it is bad-style, 
	## and would be slow to support in javascript.
	#assert( f2( 100 ) == 102 )


	## GOTCHA: below is valid in Python, but not in Rusthon,
	## this is bad-style because the caller is enforcing
	## a naming convention on the function, and in typical
	## python code named parameters are only used when
	## the function has been defined with named keywords.
	## allowing this would also allow for bad-style that
	## would break when calling js functions from external libs.
	#assert( f1( a=100 ) == 100 )

	print 'ok'

main()
