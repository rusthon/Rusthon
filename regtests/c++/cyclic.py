'''
detect cyclic parent/child, and insert weakref
'''
class Parent:
	def __init__(self, children:[]Child ):
		self.children = children

	def create_child(self, x:int):
		child = Child(x, self)
		self.children.append( child )

class Child:
	def __init__(self, x:int, parent:Parent ):
		self.x = x
		self.parent = parent

	def foo(self) ->int:
		return self.x * 2


def main():
	#children = []Child(None,None)
	children = []Child()
	p = Parent( children )
	p.create_child(1)
	p.create_child(2)
	p.create_child(3)
