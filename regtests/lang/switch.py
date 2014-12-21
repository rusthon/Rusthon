'''
switch case default
'''

def main():
	## this is ok in rust because it can infer the type of x from below,
	## but this fails with the C++ backend because None becomes std::nullptr
	#x = None
	x = ''
	a = 2
	switch a:
		case a==1:
			x = 'fail'
		case a==2:
			x = 'ok'
		default:
			## default x to some string so that rust can see that x is a string in all cases,
			## this is only required if x was initalized to None
			x = 'default'
			break
	print(x)
	TestError( x=='ok' )

