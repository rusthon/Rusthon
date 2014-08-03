"""a <- """
import go

def main():
	c = go.make_channel(int)
	 
	def wrapper(a:int, chan c:int):
		result = longCalculation(a)
		c <- result

	go( wrapper(17, c) )

	# Do other work in the current goroutine until the channel has a result.

	x = <-c
	print(x)
