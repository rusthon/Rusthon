'''
return a class instance
'''

class A: pass

def create_A() -> A:
	a = A()
	return a

def main():
	x = create_A()
	print(x)
