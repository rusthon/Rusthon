'''
simple globals
'''

class A: pass

let a : A = None
b = 0

def check_globals():
	print('a addr:', a)  ## should not print `0`
	print('b value:', b)

def main():
	global a, b
	check_globals()
	a = A()
	print(a)
	print(a.__class__)
	b = 100
	check_globals()
