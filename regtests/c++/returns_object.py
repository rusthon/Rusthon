'''
return a class instance
'''

class A:
	def __init__(self, x:int, y:int):
		self.x = x
		self.y = y

def create_A() -> A:
	a = A(1,2)
	return a

def main():
	x = create_A()
	print(x)
	print(x.x)
	print(x.y)
