"""shared list"""

import threading

def webworker(a):
	## In CPython this decorator does nothing.
	## In PythonJS this decorator name is special,
	## and triggers special code injected into the
	## header of the function, and saves the worker
	## function in a file "xxx.js" and in the main
	## script the function is changed to a string
	return lambda f : f

@webworker( 'xxx.js' )
def mythread(a,b):
	## checks a and b, if they are Array, then wrap them.
	print(a)
	print(b)
	a.append('hello')

	b.append('world')
	b.append( 'XXX' )

	## this fails if the worker is translated in javascript-mode because the method __setitem__ is not called,
	## and instead b[1] is used directly.
	b[1] = 'YYY'

def main():
	if PYTHON != "PYTHONJS":
		threading.start_new_thread = threading._start_new_thread

	shared1 = []
	shared2 = []

	t = threading.start_new_thread( mythread, (shared1, shared2) )

	ticks = 0
	while len(shared1) + len(shared2) < 2:
		ticks += 1

	TestError( shared1[0] == 'hello' )
	TestError( shared2[0] == 'world' )
	TestError( shared2[1] == 'YYY' )
