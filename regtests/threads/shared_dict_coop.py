'''
threads shared dict
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

	seq = {}
	w1 = threading.start_webworker( worker, (seq, 'abcdefgh', 'i') )
	w2 = threading.start_webworker( worker, (seq, 'ijklmnop', 'p') )
	sleep(1.0)


	TestError( 'a' in seq )
	TestError( 'i' in seq )
	print('-----main exit')
	print(seq)

if PYTHON != 'PYTHONJS':
	class webworker(object):
		def __enter__(self, *args): pass
		def __exit__(self, *args): pass
	webworker = webworker()

with webworker:
	def worker(seq, s, break_on):
		print('------enter worker------')
		for char in s:
			seq[ char ] = True
			if break_on in seq:
				break
		#while break_on not in seq:
		#	seq[ '-' ] = False
		sleep(0.1)  # this sleep is not required in normal CPython

		print('worker exit')
		print(seq)

