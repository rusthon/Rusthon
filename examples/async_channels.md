Async Channels
---------------

Below works with the C++ and Go backends.
Channels are implemented in C++ using [cpp-channel](https://github.com/ahorn/cpp-channel).

See the Wiki doc for more info on channels and spawn [here](https://github.com/rusthon/Rusthon/wiki/concurrency).

```rusthon
#backend:c++

def sender_wrapper(a:int, send: chan int ):
	print 'sending'
	result = 100
	send <- result

def recv_wrapper(a:int, recver: chan int ) -> int:
	print 'receiving'
	v = <- recver
	return v

def main():
	print 'enter main'
	c = channel(int)
	spawn( sender_wrapper(17, c) )
	x = recv_wrapper(2, c)
	print(x)
	print 'ok'
```

