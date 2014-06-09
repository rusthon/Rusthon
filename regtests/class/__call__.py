"""custom callable"""

class A:
	def __init__(self):
		self.x = 5
	def __call__(self):
		return 'XXX'


def main():
	a = A()
	TestError(a.x == 5)
	TestError( a()=='XXX' )