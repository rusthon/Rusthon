'''
detect cyclic parent/child, and insert weakref
'''
class Parent:
	def __init__(self, y:int, children:[]Child ):
		self.children = children
		self.y = y

	def create_child(self, x:int, parent:Parent) ->Child:
		child = Child(x, parent)
		self.children.push_back( child )
		return child

	def say(self, msg:string):
		print(msg)

class Child:
	def __init__(self, x:int, parent:Parent ):
		self.x = x
		self.parent = parent

	def foo(self) ->int:
		'''
		It is also valid to use `par=self.parent`,
		but it is more clear to use `weakref.unwrap(self.parent)`
		'''
		par = weak.unwrap(self.parent)
		if par is not None:
			return self.x * par.y
		else:
			print('parent is gone..')

	def bar(self):
		'''
		below `self.parent` is directly used in expressions,
		and not first assigned to a variable.
		for each use of self.parent the weakref will be promoted
		to a shared pointer, and then fall out of scope, 
		which is slower than above.
		'''
		self.parent.say('hello parent')
		print(self.parent.y)


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