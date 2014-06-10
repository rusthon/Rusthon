"""custom addition"""

class A:
	def __init__(self):
		self.x = 5
	def __add__(self, other):
		return self.x + other.x


def main():
	a = A()
	b = A()
	c = a + b
	TestError( c == 10 )

