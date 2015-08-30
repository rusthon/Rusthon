"""cpp-channel backend - send int over channel"""

def sender_wrapper(a:int, send: chan int ):
	## `chan T` is an alias for `cpp::channel<T>`
	print 'sending'
	result = 100
	send <- result

def recv_wrapper(a:int, recver: cpp::channel<int> ) -> int:
	## above namespace and template are given c++ style to recver
	print 'receiving'
	v = <- recver
	return v

def main():
	print 'enter main'
	c = channel(int)  ## `channel(T)` translates to: `cpp::channel<T>`
	print 'new channel'
	## spawn creates a new std::thread, 
	## and joins it at the end of the function.
	print 'doing spawn thread'
	spawn( sender_wrapper(17, c) )
	print 'done spawning thread'
	# Do other work...
	x = recv_wrapper(2, c)
	print(x)
	assert x==100
	print 'ok'