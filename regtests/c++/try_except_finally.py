'''
c++ finally
'''

def myfunc():
	b = False
	try:
		print('trying something that will fail...')
		print('some call that fails at runtime')
		f = open('/tmp/nosuchfile')
	except:
		print('got exception')
	finally:
		print('finally cleanup')
		b = True

	TestError( b == True )

def main():
	myfunc()
