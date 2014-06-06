"""shared list"""

import threading


@webworker( 'xxx.js' )
def mythread(a,b):
	## checks a and b, if they are Array, then wrap them.
	a.append('hello')
	b.append('world')
	b.append( 'XXX' )

	## this fails if the worker is translated in javascript-mode because the method __setitem__ is not called,
	## and instead b[1] is used directly.
	b[1] = 'YYY'

	ticks = 0
	while True: #'ZZZ' not in a:
		ticks += 1
		if ticks > 100000:
			break
		if 'ZZZ' in a:
			break

def main():

	shared1 = []
	shared2 = []

	t = threading.start_new_thread( mythread, (shared1, shared2) )

	ticks = 0
	while len(shared1) + len(shared2) < 4:
		ticks += 1
		if ticks > 100000:  ## do not hangup if there is a bug in the webworker
			break

	shared1.append( 'ZZZ' )

	TestError( shared1[0] == 'hello' )
	TestError( shared2[0] == 'world' )
	TestError( shared2[1] == 'YYY' )

	ticks = 0
	while ticks < 100000:
		ticks += 1
