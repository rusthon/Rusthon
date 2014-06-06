"""int static type"""
from time import time

def F(i, n, arr):
	int i
	list arr
	while i < n:

		arr.append( i*2 )
		arr.append( i*4 )
		arr.append( i*8 )
		arr.append( i*16 )
		arr.append( i*32 )
		arr.append( i*64 )
		arr.append( i*128 )
		arr.append( i*256 )
		arr.append( i*512 )
		arr.append( i*1024 )
		arr.append( i*2048 )
		arr.append( i*4096 )

		arr.append( i//2 )
		arr.append( i//4 )
		arr.append( i//8 )
		arr.append( i//16 )
		arr.append( i//32 )
		arr.append( i//64 )
		arr.append( i//128 )
		arr.append( i//256 )
		arr.append( i//512 )
		arr.append( i//1024 )
		arr.append( i//2048 )
		arr.append( i//4096 )

		for x in range(100):
			arr.append( i+x )

		i += 1


def main():
	start = time()
	F(0, 10000, [])
	F(0, 10000, [])
	F(0, 10000, [])
	print( time()-start )
