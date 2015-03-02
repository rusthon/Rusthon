Async Channels Rust
-----

Rust has builtin async channels, but the `Sender` and `Receiver` are different types.
This syntax is also compatible with the C++ and Go backends, but `chan Sender<T>` and `chan Receiver<T>` has no extra meaning, they are simply two way channels.

```rusthon
#backend:rust

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
	x = recv_wrapper(2, recver)
	print(x)
```