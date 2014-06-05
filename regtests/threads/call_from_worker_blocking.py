'''call function from main and get result'''
import threading
from time import sleep

shared = []

def blocking_func(x,y):
	shared.append( x )
	shared.append( y )
	return x+y

def async_func( a ):
	shared.append( a )

def main():
	w = threading.start_webworker( worker, [] )
	sleep(1.0)

	TestError( len(shared)==3 )
	TestError( shared[0]==10 )
	TestError( shared[1]==20 )
	TestError( shared[2]==30 )


with webworker:

	def worker():
		## the translator knows this is blocking because the result of the function is assigned to `v`,
		v = blocking_func( 10, 20 )
		#print('returned to blocking callback', v)
		async_func( v )
		self.terminate()
