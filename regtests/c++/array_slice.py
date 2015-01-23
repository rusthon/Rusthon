'''
array slice syntax
'''


def main():
	#a = [1,2,3,4,5]
	a = []int(1,2,3,4,5)
	print('a addr:', a)
	print('len a:', len(a))
	b = a[1:]
	print('b addr:', b)
	print('len b:', len(b))

	c = a[:]
	print('len c:', len(c))
	c.push_back(6)
	print('len c - after append:', len(c))
	print('len a:', len(a))

	print('end slice test')