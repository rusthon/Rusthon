'''
loop and add (integer)
'''

from time import time
from time import sleep
import threading

#PYTHON = 'O'

def main():
	if PYTHON=='PYTHONJS':
		pythonjs.configure( direct_operator='+' )
		pass
	else:
		l = lambda f,a,name=None: threading._start_new_thread(f,a)
		threading.start_webworker = l

	start = time()
	n = 600
	seq = []
	cache = {}

	#w = worker(n,seq, cache)
	w1 = threading.start_webworker( worker, (0, n, seq, cache) )
	w2 = threading.start_webworker( worker, (1, n, seq, cache) )
	sleep(1.0)

	print(time()-start)
	print(len(seq))
	#seq.sort()
	print(seq)
	print('-----main exit')

if PYTHON != 'PYTHONJS':
	class webworker(object):
		def __enter__(self, *args): pass
		def __exit__(self, *args): pass
	webworker = webworker()

with webworker:
	def worker(start, end, seq, cache):
		print('------enter worker------')
		for i in range(start, end):
			if i in cache:
				continue
			else:
				cache[i] = None  ## prevent other worker from doing same job
				if is_prime(i):
					seq.append( i )
					cache[i] = True
				else:
					cache[i] = False
		print('worker exit-------')

	def is_prime(n):
		hits = 0
		for x in range(2, n):
			for y in range(2, n):
				if x*y == n:
					hits += 1
					if hits > 1:
						return False
		return True


#main()