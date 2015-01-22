Array Generics
--------------
Below `if isinstance` is used to cast item to that type, if it is an instance of that class.

```rusthon
class A:
	def __init__(self, x:int):
		self.x = x
	def method1(self) -> int:
		return self.x

class B(A):
	def method1(self) ->int:
		return self.x * 2
	def method2(self, y:int):
		print( self.x + y )

class C(A):
	def method1(self) ->int:
		return self.x + 200
	def say_hi(self):
		print('hi from C')

def main():
	a = A( 1 )
	b = B( 200 )
	c = C( 3000 )
	arr = []A( a,b,c )

	for item in arr:
		print(item.method1())

		if isinstance(item, B):
			item.method2( 20 )

		if isinstance(item, C):
			item.say_hi()
```