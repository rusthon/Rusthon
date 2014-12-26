"""go select"""

def send_data( A:chan int, B:chan int, X:int, Y:int):
	while True:
		print('sending data..')
		A <- X
		B <- Y

def select_loop(A:chan int, B:chan int, W:chan int) -> int:
	print('starting select loop')
	y = 0
	while True:
		print('select loop:',y)
		select:
			case x = <- A:
				y += x
				W <- y
			case x = <- B:
				y += x
				W <- y
	print('end select loop', y)
	return y

def main():
	a = go.channel(int)
	b = go.channel(int)
	w = go.channel(int)

	go(
		select_loop(a,b, w)
	)


	go(
		send_data(a,b, 5, 10)
	)

	z = 0
	while z < 100:
		z = <- w
		print('main loop', z)

	print('end test')