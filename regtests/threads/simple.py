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
def mythread(a):
	for i in range(100):
		a.append( i )

def main():
	if PYTHON != "PYTHONJS":
		threading.start_new_thread = threading._start_new_thread

	arr = []
	t = threading.start_new_thread( mythread, (arr,) )
	ticks = 0
	while len(arr) < 100:
		ticks += 1
		if ticks > 1000:  ## do not hangup if there is a bug in the webworker
			break

	TestError( sum(arr) == 4950 )
