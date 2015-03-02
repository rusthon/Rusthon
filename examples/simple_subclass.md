Subclass Example
----------------
overload method of parent, also calls parent method from subclass overload, `BaseClass.method(self)`
note this is old style python where the base class is used directly, the `super` special call is not supported.

```rusthon
#backend:c++

class Vec2:
	def __init__(self, x:f32=0.0, y:f32=0.0):
		self.x = x
		self.y = y

	def sum(self) ->f32:
		return self.x + self.y

class Vec3( Vec2 ):
	def __init__(self, z:f32):
		Vec2.__init__(self, x=400.0, y=20.0)
		self.z = z

	def sum(self) ->f32:
		return Vec2.sum(self) + self.z


def main():
	v = Vec3( 100.0 )
	print v.sum()

```