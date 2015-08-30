'''
c++ finally
'''

def myfunc():
	## TODO - update __open__ so it throws an error
	f = open('/tmp/nosuchfile')

	b = False

	try:
		print('trying something that will fail...')
		print('some call that fails at runtime')
		f = open('/tmp/nosuchfile')
	except:
		print('CAUGHT EXECEPTION')
	finally:
		print('finally cleanup')
		b = True

	assert b == True

def main():
	myfunc()
