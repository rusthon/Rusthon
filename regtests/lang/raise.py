'''
raise and catch error
'''

def main():
	a = False
	try:
		raise TypeError
	except TypeError:
		a = True

	TestError( a==True )

	b = False
	try:
		b = True
	except:
		b = False

	TestError( b==True )

	c = False
	try:
		raise AttributeError('name')
	except AttributeError:
		c = True

	TestError( c==True )
