C++ Operator Overloading
------------

class A shows how to define subscript `a[key]`, define a method named `__getitem__` that takes the key and returns a value.
class MyVec shows how to overload the `+` operator, note the use of `.pointer` is used to deference the pointer.

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



def main():
	d = map[string]int{'hello':1, 'world':2}
	a = A(d)
	print a['hello']
	print a['world']

	v1 = MyVec(1,2,3)
	v2 = MyVec(100,200,300)
	v1.show()
	v1.pointer += v2
	v1.show()
	v3 = v1.pointer + v2
	v3.show()

```