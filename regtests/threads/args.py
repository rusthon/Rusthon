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
def mythread(a,b):
	print(a)
	print(b)
	threading.shared_list.append( a )
	threading.shared_list.append( b )

def main():
	if PYTHON != "PYTHONJS":
		threading.start_new_thread = threading._start_new_thread
		threading.shared_list = list()

	t = threading.start_new_thread( mythread, ('hello', 'worker') )
	ticks = 0
	while len(threading.shared_list) < 2:
		ticks += 1

	TestError( threading.shared_list[0] == 'hello' )
	TestError( threading.shared_list[1] == 'worker' )
