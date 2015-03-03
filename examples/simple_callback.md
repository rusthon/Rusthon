Callback Functions/Methods
----------------

Note: `|` is used to separate multiple argument types in a `lambda()()` callback typedef.

```rusthon
#backend:c++

class Vec2:
	def __init__(self, x:f32, y:f32):
		self.x = x
		self.y = y

	def add(self, x:f32, y:f32):
		self.x += x
		self.y += y

	def show(self):
		print self.x
		print self.y


def call_method( callback:lambda(f32|f32)(), other:Vec2 ):
	callback( other.x, other.y )


def main():
	v1 = Vec2( 1.0, 2.0 )
	v2 = Vec2( 100.0, 200.0 )

	call_method(
		lambda x=f32, y=f32: v1.add(x,y), 
		v2 
	)
	v1.show()

```