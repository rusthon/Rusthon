'''call function in main from inside webworker'''
import threading
from time import sleep

shared = []

def myfunc( a, b ):
	shared.append( a )
	shared.append( b )

def main():
	w = threading.start_webworker( worker, [] )
	sleep(1.0)

	TestError( len(shared)==2 )
	TestError( shared[0]==10 )
	TestError( shared[1]==20 )


with webworker:

	def worker():
		myfunc( 10, 20 )
