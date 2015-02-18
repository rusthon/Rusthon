'''
detect cyclic parent/child, and insert weakref
'''
class Parent:
	def __init__(self, children:[]Child ):
		self.children = children

class Child:
	def __init__(self, parent:Parent ):
		self.parent = parent

	def foo(self) ->int:
		par = self.parent
		if par is not None:
			return 1
		else:
			print('parent is gone..')

	def bar(self):
		print self.parent.children

def make_child(p:Parent) -> Child:
	c = Child(p)
	p.children.push_back(c)
	return c


def main():
	children = []Child()
	p = Parent( children )
	c1 = make_child(p)
	c2 = make_child(p)
	print c1.foo()
	c1.bar()
	del p
	print c1.foo()
	#uncomment to segfault##c1.bar()