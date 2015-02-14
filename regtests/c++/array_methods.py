'''
array methods: append, pop, etc.
'''

def somefunc():
	a = []int(1,2,3,4,5)
	print('len a:', len(a))
	#b = a.pop()
	b = a[len(a)-1]
	a.pop()
	print('len a:', len(a))
	print(b)

def main():
	somefunc()
	print('OK')