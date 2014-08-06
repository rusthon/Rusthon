"""go select"""

def main():
	a = go.channel(int)
	b = go.channel(int)

	a <- 1
	b <- 2
	y = 0

	select:
		case x = <- a:
			y += x
		case x = <- b:
			y += x

	print(y)
