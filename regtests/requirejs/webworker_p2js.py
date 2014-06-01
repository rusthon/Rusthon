'''import p2.js inside webworker'''
# sudo npm install -g p2
import threading
from time import sleep

def main():
	shared = []
	w = threading.start_webworker( worker, [shared] )
	sleep(1.0)

	TestError( len(shared)==2 )
	TestError( shared[0]==10 )
	TestError( shared[1]==20 )


with webworker:
	import p2

	def worker( arr ):
		v = p2.vec2.fromValues(10,20)
		arr.append( v[0] )
		arr.append( v[1] )
