"""simple thread"""

import threading


@webworker( 'myworker.js' )
def mythread(a):
	for i in range(100):
		a.append( i )

def main():

	arr = []
	t = threading.start_new_thread( mythread, (arr,) )
	ticks = 0
	while len(arr) < 100:
		ticks += 1
		if ticks > 100000:  ## do not hangup if there is a bug in the webworker
			break

	TestError( sum(arr) == 4950 )
