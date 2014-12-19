'''
rust try!
'''

def myfunc():
	b = False
	try:
		print('trying something that will fail...')
		print('some call that fails at runtime')
	except:
		b = True

	TestError( b == True )

def main():
	myfunc()
