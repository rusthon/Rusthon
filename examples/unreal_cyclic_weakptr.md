Unreal Engine Smart Pointers
------------------

https://docs.unrealengine.com/latest/INT/Programming/UnrealArchitecture/SmartPointerLibrary/WeakPointer/index.html

@unrealtypes.json
```json
{
	"vector"   : {
		"template": "TArray<%s>",
		"append"  : "Emplace",
		"len"     : "Num"
	},
	"string" : {
		"type": "FString",
		"new" : "TEXT(%s)"
	},
	"shared" : {
		"template" : "TSharedRef<%s>",
		"type"     : "TSharedRef",
		"reset"    : "Reset"
	},
	"weakref": {
		"template": "TWeakPtr<%s>",
		"type": "TWeakRef",
		"lock": "Lock",
		"reset": "Reset",
		"valid": "IsValid"
	}
}
```


```rusthon
with syntax('unrealtypes.json'):
	class Parent:
		def __init__(self, y:int, children:[]Child ):
			self.children = children
			self.y = y

		def say(self, msg:string):
			print(msg)

```
the pointer to parent here in `self.parent` becomes a `TWeakRef`.
note children can not contain a list of multiple parents, 
but could have more than one parent if each had its own name like: `self.parent1` and `self.parent2`.

```rusthon
	class Child:
		def __init__(self, x:int, parent:Parent ):
			self.x = x
			self.parent = parent

		def foo(self) ->int:
			par = self.parent
			#if par is not None:
			if weak.valid(par):
				return self.x * par.y
			else:
				print('parent is gone..')

		def bar(self):
			'''
			this works even after parent is destroyed,
			because the function is pure and not dependent on the state of the pointer.
			'''
			self.parent.say('hello parent')

		def crashes(self):
			a = self.parent.y
			print a

```

function that makes a new child object and returns it
note: the c++ vector function `push_back` is used directly, instead of the python style `append`.

```rusthon
	def make_child(p:Parent, x:int) -> Child:
		c = Child(x, p)
		p.children.push_back(c)
		return c
```

main entry point.

```rusthon

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

		print 'calling foo'
		print c1.foo()
		print 'calling bar'
		c1.bar()

		del p
		print c1.foo()
		c1.bar()
		#uncomment to segfault#c1.crashes()
```