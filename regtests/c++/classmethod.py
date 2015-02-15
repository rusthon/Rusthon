'''
class methods
'''
class A:
	def __init__(self, x:int, y:int):
		self.x = x
		self.y = y

	@classmethod
	def foo(self):
		print('my classmethod')

	@classmethod
	def bar(self, a:int) ->int:
		return a+1000

def main():
	x = A(1,2)
	x.foo()
	A.foo()
	print x.bar( 100 )
	y = A.bar(200)
	print(y)
