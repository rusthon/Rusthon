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
