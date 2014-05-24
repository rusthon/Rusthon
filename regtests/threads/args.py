"""simple thread"""

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
def mythread(a,b, c):
	print(a)
	print(b)
	c.append( a )
	c.append( b )

def main():
	if PYTHON != "PYTHONJS":
		threading.start_new_thread = threading._start_new_thread
		threading.shared_list = list()

	c = []
	t = threading.start_new_thread( mythread, ('hello', 'worker', c) )
	ticks = 0
	while len(c) < 2:
		ticks += 1
		if ticks > 1000:  ## do not hangup if there is a bug in the webworker
			break

	TestError( c[0] == 'hello' )
	TestError( c[1] == 'worker' )
