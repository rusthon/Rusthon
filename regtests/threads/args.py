"""simple thread"""
from time import sleep
import threading

@webworker( 'xxx.js' )
def mythread(a,b, c):
	c.append( a )
	c.append( b )

def main():

	c = []
	t = threading.start_new_thread( mythread, ('hello', 'worker', c) )
	sleep(0.1)
	ticks = 0
	while len(c) < 2:
		ticks += 1
		if ticks > 100000:  ## do not hangup if there is a bug in the webworker
			break

	TestError( c[0] == 'hello' )
	TestError( c[1] == 'worker' )
