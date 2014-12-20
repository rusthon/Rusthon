'''
rust try!
'''

def myfunc():
	b = False
	try:
		print('trying something that will fail...')
		print('some call that fails at runtime')
		f = open('/tmp/nosuchfile')
	except:
		b = True

	#print('trying something that will fail...')
	#print('some call that fails at runtime')
	#f = open('/tmp/nosuchfile')


	TestError( b == True )

def main():
	myfunc()
