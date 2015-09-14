from runtime import *
'''
try except
'''

def main():
	a = [1,2,3]
	b = False
	try:
		a.no_such_method()
		b = 'this should not happen'
	except:
		b = True
	assert( b == True )


main()
