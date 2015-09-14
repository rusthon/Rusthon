from runtime import *
'''
==
'''
# https://github.com/PythonJS/PythonJS/issues/129

def main():
	assert( 0==0 )
	assert( 1==1 )
	assert( 1.0==1 )
	assert('a'=='a')


	a = [6]
	b = [6]
	#t = a==b  ## this works in regular python
	t1 = a.equals(b)
	assert( t1==True )

	a = (6,)
	b = (6,)
	#t = a==b
	t2 = a.equals(b)
	assert( t2==True )

	t3 = ''==0  ## javascript gotcha, workaround: `len('')==0`
	print 'empty string equals zero:' + t3
	#assert( t==False )

	t4 = [1,2].equals([1,2])
	assert( t4==True )

	t5 = ["1","2"].equals([1,2])
	assert( t5==False )


main()
