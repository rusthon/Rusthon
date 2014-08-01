'''
==
'''
# https://github.com/PythonJS/PythonJS/issues/129

def main():
	TestError( 0==0 )
	TestError( 1==1 )
	TestError( 1.0==1 )
	TestError('a'=='a')


	a = [6]
	b = [6]
	t = a==b
	TestError( t==True )

	a = (6,)
	b = (6,)
	t = a==b
	TestError( t==True )

	t = ''==0  ## javascript gotcha
	TestError( t==False )

	t = [1,2]==[1,2]  ## javascript gotcha
	TestError( t==True )

	t = ["1","2"] != [1,2]  ## javascript gotcha
	TestError( t==True )

