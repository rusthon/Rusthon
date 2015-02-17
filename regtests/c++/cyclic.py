'''
detect cyclic parent/child, and insert weakref
'''
class Parent:
	def __init__(self, y:int, children:[]Child ):
		self.children = children
		self.y = y

	def create_child(self, x:int, parent:Parent) ->Child:
		#child = Child(x, self)  ## TODO fix me
		#self.children.append( child )  ## TODO fix me

		child = Child(x, parent)
		self.children.push_back( child )
		return child

class Child:
	def __init__(self, x:int, parent:Parent ):
		self.x = x
		self.parent = parent

	def foo(self) ->int:
		'''
		must call unwrap on the weak_ptr to get a shared pointer,
		and make sure it is not None.
		'''
		par = unwrap(self.parent)
		if par is not None:
			return self.x * par.y
		else:
			print('parent is gone..')


def main():
	#children = []Child(None,None)
	children = []Child()
	p = Parent( 1000, children )
	print 'parent:', p

	c1 = p.create_child(1, p)
	c2 = p.create_child(2, p)
	c3 = p.create_child(3, p)
	print 'children:'
	print c1
	print c2
	print c3