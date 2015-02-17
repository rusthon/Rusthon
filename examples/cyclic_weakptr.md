C++ Smart Pointers
------------------
std::shared_ptr with automatic setup of std::weak_ptr.
the parent class must contain a list of child objects.

```rusthon
class Parent:
	def __init__(self, y:int, children:[]Child ):
		self.children = children
		self.y = y

	def say(self, msg:string):
		print(msg)

class Child:
	def __init__(self, x:int, parent:Parent ):
		self.x = x
		self.parent = parent

	def foo(self) ->int:
		par = self.parent
		if par is not None:
			return self.x * par.y
		else:
			print('parent is gone..')

	def bar(self):
		print(self.parent.y)
		self.parent.say('hello parent')

def make_child(p:Parent, x:int) -> Child:
	c = Child(x, p)
	p.children.push_back(c)
	return c

def main():
	children = []Child()
	p = Parent( 1000, children )
	print 'parent:', p

	c1 = make_child(p, 1)
	c2 = make_child(p, 20)
	c3 = make_child(p, 300)
	print 'children:'
	print c1
	print c2
	print c3

	c1.foo()
	c1.bar()

	del p
	c1.foo()
```