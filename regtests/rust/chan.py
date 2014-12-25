"""rust send int over channel"""

def wrapper(a:int, c: chan int):
	result = 100
	c <- result

def main():
	sender, recver = go.channel(int)

	go( wrapper(17, sender) )

	# Do other work in the current goroutine until the channel has a result.

	x = <-recver
	print(x)
	TestError(x==100)
