'''
array slice assignment syntax
'''

def somefunc():
	a = [1,2,3,4,5]
	b = [6,7,8,9,10]
	print('len a:', len(a))
	for i in a:
		print i

	a[:2] = b
	print('len a:', len(a))
	for i in a: print i


def main():
	somefunc()
