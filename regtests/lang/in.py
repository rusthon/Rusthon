'''
in (contains)
'''

def func( word, custom={} ):
	if word in custom:
		return True
	else:
		return False

def main():
	TestError( func('x', custom={'x':1})==True )

	TestError( func('y', custom={'x':1})==False )


