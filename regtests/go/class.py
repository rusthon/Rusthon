'''
simple class
'''
class A:
	{
		x:int,
		y:int,
	}
	def __init__(self):
		self.x = 1
		self.y = 2

def main():
	a = A()
	print( a.x )