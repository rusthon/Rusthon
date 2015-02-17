'''
detect cyclic parent/child, and insert weakref
'''
class Parent:
	def __init__(self, y:int, children:[]Child ):
		self.children = children
		self.y = y

	def create_child(self, x:int, parent:Parent) ->Child:
		#child = Child(x, self)
		#self.children.append( child )

		child = Child(x, parent)
		self.children.push_back( child )
		return child

class Child:
	def __init__(self, x:int, parent:Parent ):
		self.x = x
		self.parent = parent

	def foo(self) ->int:
		'''
		must call lock on weak_ptr to get a shared pointer
		'''
		#par = self.parent.lock()  ## fails because this->parent->lock() should be this->parent.lock()
		par = unwrap(self.parent)
		if par is not None:
			return self.x * par.y
		else:
			print('parent is gone..')


def main():
	#children = []Child(None,None)
	children = []Child()
	p = Parent( 1000, children )
	p.create_child(1, p)
	p.create_child(2, p)
	p.create_child(3, p)
