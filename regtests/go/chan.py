"""a <- """

def main():
	c = go.channel(int)
	 
	def wrapper(a:int, chan c:int):
		result = 100
		c <- result

	go(
		wrapper(17, c)
	)

	# Do other work in the current goroutine until the channel has a result.

	x = <-c
	print(x)
