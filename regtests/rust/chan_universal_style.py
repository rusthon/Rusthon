"""send int over channel for rust, go, and c++"""

def sender_wrapper(a:int, send: chan Sender<int> ):
	result = 100
	send <- result

def recv_wrapper(a:int, recver: chan Receiver<int> ) -> int:
	v = <- recver
	return v

def main():
	## sender and recver are the same object in Go and C++
	sender, recver = channel(int)
	spawn( sender_wrapper(17, sender) )
	# Do other work in the current goroutine until the channel has a result.
	x = recv_wrapper(2, recver)
	print(x)
	assert x==100
