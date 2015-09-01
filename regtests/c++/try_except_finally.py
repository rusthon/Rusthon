'''
c++ finally
'''

def myfunc():

	a = False
	try:
		raise RuntimeError('oops')
	except RuntimeError:
		print 'caught RuntimeError OK'
		a = True

	assert a == True


	c = False
	try:
		raise IOError('my ioerror')

	except IOError as err:
		print 'caught my ioerr'
		print err.what()
		#raise err  ## rethrow works ok
		c = True
	assert c == True


	b = False

	try:
		print('trying something that will fail...')
		print('some call that fails at runtime')
		f = open('/tmp/nosuchfile')
	except RuntimeError:
		print 'this should not happen'
	except IOError:
		print 'CAUGHT IOError OK'
		## it is ok to raise or return in the except block,
		## the finally block will be run before any of this happens
		#raise RuntimeError('rethrowing error')  ## this works
		return

	except:
		print('CAUGHT UNKNOWN EXECEPTION')
		## raise another exception
		raise RuntimeError('got unknown exception')
	finally:
		print('FINALLY')
		b = True

	assert b == True





def main():
	myfunc()
