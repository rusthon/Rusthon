"""shared list"""
from time import sleep
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
	print('------enter thread------')
	for i in range(10):
		a.append('o')
		#sleep(0.01)
	
	print(a)
	print('thread exit-------')

def main():
	if PYTHON != "PYTHONJS":
		threading.start_new_thread = threading._start_new_thread

	shared1 = []
	shared2 = []

	t = threading.start_new_thread( mythread, (shared1, shared2) )
	i = 0
	while i < 10:
		shared1.append('x')
		i += 1
		sleep(0.01)

	TestError( len(shared1) == 20 )
	print('_____')
	print(shared1)
	print('-----main exit')