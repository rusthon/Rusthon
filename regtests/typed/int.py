"""int static type"""


def main():
	int x = 1
	y = x + x
	TestError( y==2 )

	int z = 2
	w = z * 2
	TestError( w==4 )

	w = z * 3
	TestError( w==6 )

	w = z * 64
	TestError( w==128 )

	w = z // 2
	TestError( w==1 )

	z = 640
	w = z // 64
	TestError( w==10 )