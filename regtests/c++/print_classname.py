'''
returns subclasses
'''
class A:
	def __init__(self, x:int):
		self.x = x

	def method(self) -> int:
		return self.x

class B(A):

	def foo(self) ->int:
		return self.x * 2

class C(A):

	def bar(self) ->int:
		return self.x + 200


def main():
	a = A(0)
	b = B(1)
	c = C(2)
	print(a.getclassname())
	print(b.getclassname())
	print(c.getclassname())


