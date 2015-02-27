C++ Operator Overloading
------------

class A shows how to define subscript `a[key]`, define a method named `__getitem__` that takes the key and returns a value.
Because subscripting always triggers the pointer to be deferenced, it works without any gotchas.

```rusthon
#backend:c++

class A:
	def __init__(self, m:map[string]int ):
		self.m = m

	def __getitem__(self, key:string) -> int:
		return self.m[ key ]

	## TODO
	#def __setitem__(self, key:string, value:int):
	#	self.m[key] = value
```


There is a gotcha with overloading binary operators: `+`, `-`, `*`, and `\`, they do not automatically deference their operands,
because normally these operations happen on primitive types, and not wrapped with a pointer.
For the simple case where the left operand is a local variable known to be of some class, Rusthon will deference it automatically.
Other cases where the left operand is unknown, the user must manually deference the pointer using `a[...]` ellipsis.


```rusthon
class MyVec:
	def __init__(self, x:int, y:int, z:int):
		self.x = x
		self.y = y
		self.z = z

	def __iadd__(self, other:MyVec):
		self.x += other.x
		self.y += other.y
		self.z += other.z

	def __add__(self, other:MyVec) ->MyVec:
		return MyVec(
			self.x+other.x,
			self.y+other.y,
			self.z+other.z,
		)

	def show(self):
		print self.x
		print self.y
		print self.z

```

__unwrap__ overloads the c++ operator `->` deference.
__copy__ overloads the c++ operator '=' copy.
This can be used for making custom pointer-like objects.

```
class MyProxy:
	def __init__(self, id:int):
		self.id = id
	def __unwrap__(self) ->MyVec:
		print 'unwrap MyProxy'
		return MyVec(0,0,0)
	def __copy__(self, p:MyProxy) ->MyProxy:
		print 'copy MyProxy', self.id
		print 'other:', p.id
		return MyProxy(3)


def myfunc( v:MyVec ):
	v.show()

```

Overloading `__call__` also has the same problem, because Rusthon expects a function and not a pointer, you must manually deference
before calling the object `myob[...]()`.  
Note: this will be fixed in Rusthon2.0 with a complete typing system that keeps track of pointers and their types.


```rusthon

class VecContainer:
	def __init__(self, somevec:MyVec):
		self.somevec = somevec
	def __call__(self, x:int=0, y:int=0, z:int=0):
		self.somevec.x += x
		self.somevec.y += y
		self.somevec.z += z
		self.somevec.show()
```

main entry point
---------------

```rusthon
def main():
	d = map[string]int{'hello':1, 'world':2}
	a = A(d)
	print a['hello']
	print a['world']

	v1 = MyVec(1,2,3)
	v2 = MyVec(100,200,300)
	v1.show()
	v1 += v2
	v1.show()
	v3 = v1 + v2
	v3.show()
	myfunc( v1+v2 )
	print('testing VecContainer')
	vc = VecContainer( v1 )
	vc.somevec.show()
	print('change .somevec')

```
calling an object requires a manual pointer dereference using `[...]`

```rusthon
	#vc.somevec += v2  ## this fails
	vc.somevec[...] += v2  ## must manually deference `somevec`

	print 'testing call'
	vc[...]( x=1000 )
	ptr = vc[...]
	ptr( y=1000 )
	ptr( z=1000 )

```
testing the special __unwrap__ and __copy__ overloads

```rusthon

	p1 = MyProxy(1)
	p2 = MyProxy(2)
	p1[...].show()
	print 'testing copy'
	p2[...] = p1

```