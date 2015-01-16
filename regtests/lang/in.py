'''
in (dict contains)
'''

def main():
	d = {'x':1}
	a = 'x' in d
	TestError( a==True )
	b = 'y' in d
	TestError( b==False )


