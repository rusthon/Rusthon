'''
threads shared data
'''

from time import time
from time import sleep
import threading


def main():
	if PYTHON=='PYTHONJS':
		pythonjs.configure( direct_operator='+' )
		pass
	else:
		def l (f,a): threading._start_new_thread(f,a)
		threading.start_webworker = l

	seq = []
	w1 = threading.start_webworker( worker, (seq, 'A', 'B') )
	w2 = threading.start_webworker( worker, (seq, 'B', 'A') )
	sleep(1.0)


	TestError( 'A' in seq )
	TestError( 'B' in seq )

	print('-----main exit')

if PYTHON != 'PYTHONJS':
	class webworker(object):
		def __enter__(self, *args): pass
		def __exit__(self, *args): pass
	webworker = webworker()

with webworker:
	def worker(seq, a, b):
		print('------enter worker------')
		for i in range(0, 10):
			seq.append( a )
			if b in seq:
				break
		print('worker reached: %s' %i)
		print(seq)

