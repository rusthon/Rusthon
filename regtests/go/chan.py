"""send int over channel"""

def wrapper(a:int, c: chan int):
	result = 100
	c <- result

def main():
	c = channel(int)

	spawn( wrapper(17, c) )

	# Do other work in the current goroutine until the channel has a result.

	x = <-c
	print(x)
	assert x==100
