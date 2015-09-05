'''
simple class
'''
class A:
	def __init__(self, x:int, y:int, z:int):
		self.x = x
		self.y = y
		self.z = z

	def mymethod(self, m:int) -> int:
		return self.x * m

def call_method( cb:lambda(int)(int), mx:int ) ->int:
	return cb(mx)

def main():
	a = A( 100, 200, 9999 )
	print( a.x )
	print( a.y )
	print( a.z )
	assert a.x == 100

	b = a.mymethod(3)
	print( b )

	## taking the address of a method pointer is not allowed in rust
	## http://stackoverflow.com/questions/24728394/rust-method-pointer
	##c = call_method( a.mymethod, 4 )

	c = call_method( lambda W=int: a.mymethod(W), 4 )
	print( c )