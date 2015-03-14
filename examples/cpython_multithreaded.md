CPython Threads GIL Test
-------------


@embed
```python
import thread, time

class A():
	def __init__(self):
		self.value = 0
	def run(self):
		print '-----starting run'
		while self.value < 10:
			print 'from cpython:', self.value
			self.value += 1
			time.sleep(0.1)
		print '------end run'
	def run_thread(self):
		thread.start_new_thread(self.run, ())

def make_A():
	return A()

```

note: `spawn` creates a c++11 thread.

Build Options
-------------
* @link:python2.7
* @include:/usr/include/python2.7
```rusthon
#backend:c++
import cpython

with pointers:
	def thread_runner(pyob:PyObject):
		print 'enter thread runner'
		with gil:
			pyob->run_thread()
			#pyob->run()
		print 'edit thread runner'


	def thread1( input: chan PyObject, output: chan PyObject ):
		while True:
			pyob = <- input  ## gets from main
			if pyob is None:
				print 'pyob is None'
				break
			with gil:
				v = pyob->value as int
			print 'thread1:', v
			inline('std::this_thread::sleep_for(std::chrono::milliseconds(100))')

		#for i in range(100):
		#	v = pyob->value as int
		#	print 'thread1:', v
		#	#output <- pyob  ## sends to thread2
		print 'end thread1'

	def thread2( C: chan PyObject):
		for i in range(100):
			pyob = <- C
			v = pyob->value as int
			print 'thread2:', v


def main():
	cpython.initalize()
	PyEval_InitThreads()  ## creates and locks GIL
	print 'threads init'
	mainstate = PyEval_SaveThread()  ## releases GIL
	print 'saved mainstate'

	print 'setup channels'
	input  = channel(PyObject)
	output = channel(PyObject)

	with gil:
		a = cpython.make_A()
	print 'addr of a:', a

	print 'starting thread1'
	spawn( thread_runner(a) )

	spawn(
		thread1(input, output)
	)
	#spawn(
	#	thread2(output)
	#)

	#a->run()
	#a->run_thread()

	print 'sending pyob'
	while True:
		with gil:
			v = a->value as int

		if v==10:
			break
		print 'main:', v

		input <- a
	input <- None

	print 'finalize'
	PyEval_RestoreThread( mainstate )  ## required not to segfault on exit
	cpython.finalize()

```