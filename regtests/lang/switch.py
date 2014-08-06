'''
switch case default
'''

def main():
	x = None
	a = 2
	switch a:
		case 1:
			x = 'fail'
		case 2:
			x = 'ok'
		default:
			break

	TestError( x=='ok' )

