"""rust select"""

def send_data( A:chan Sender<int>, B:chan Sender<int>, X:int, Y:int):
	while True:
		print('sending data..')
		A <- X
		B <- Y

def select_loop(A:chan Receiver<int>, B:chan Receiver<int>, W:chan Sender<int>) -> int:
	print('starting select loop')
	let x : int
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
	asender, arecver = channel(int)
	bsender, brecver = channel(int)
	wsender, wrecver = channel(int)

	t1 = spawn(
		select_loop(arecver,brecver, wsender)
	)
	t1.detach()

	t2 = spawn(
		send_data(asender,bsender, 5, 10)
	)
	t2.detach()
	
	z = 0
	while z < 100:
		z = <- wrecver
		print('main loop', z)

	print('end test')