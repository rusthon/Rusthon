from runtime import *
'''
raise and catch error
'''

def main():
	a = False
	try:
		raise TypeError
	except TypeError:
		a = True

	assert( a==True )

	b = False
	try:
		b = True
	except:
		b = False

	assert( b==True )

	c = False
	try:
		raise AttributeError('name')
	except AttributeError:
		c = True

	assert( c==True )

main()
