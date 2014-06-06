"""shared lists"""
from time import sleep
import threading

@webworker( 'myworker.js' )
def mythread(a,b):
	i = 0
	while i < 10:
		a.append('o')
		i += 1
		#sleep(0.1)
	
def main():

	shared1 = []
	shared2 = []

	t = threading.start_new_thread( mythread, (shared1, shared2) )
	i = 0
	while i < 10:
		shared1.append('x')
		i += 1
		sleep(0.2)

	while len(shared1) <= 20:
		shared1.append('0')
		sleep(0.1)

	TestError( len(shared1) == 20 )
