'''
rust try!
'''

def myfunc():
	b = False
	try:
		print('trying something that will fail...')
		print('some call that fails at runtime')
		#f = open('/tmp/nosuchfile')
		raise RuntimeError()
	except:
		b = True

	TestError( b == True )
	print('ok')

def main():
	myfunc()
