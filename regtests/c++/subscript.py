'''
simple subscript
'''


def main():
	a = []int(1,2,3)
	index = 0
	a[ index ] = 100
	print(a[index])

	s = "hello world"
	print(s)
	print(s[0])
	print(s[1])
	print(s[2])
	print(s[3])
	if s[0]=='h':
		print('ok')
	else:
		print('error')
