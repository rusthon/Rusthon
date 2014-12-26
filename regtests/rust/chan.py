"""rust send int over channel"""

def sender_wrapper(a:int, send: Sender<int> ):
	result = 100
	send <- result

def recv_wrapper(a:int, recver: Receiver<int> ) -> int:
	v = <- recver
	return v

def main():
	sender, recver = go.channel(int)
	go( sender_wrapper(17, sender) )
	# Do other work in the current goroutine until the channel has a result.
	x = recv_wrapper(2, recver)
	#x = <-recver
	print(x)
	TestError(x==100)
