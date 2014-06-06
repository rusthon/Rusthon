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

	seq = []
	w1 = threading.start_webworker( worker, (seq, 'A', 'B') )
	w2 = threading.start_webworker( worker, (seq, 'B', 'A') )

	sleep(1.0)

	TestError( 'A' in seq )
	TestError( 'B' in seq )


with webworker:
	def worker(seq, a, b):
		for i in range(0, 10):
			seq.append( a )
			if b in seq:
				break

