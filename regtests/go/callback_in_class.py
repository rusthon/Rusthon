'''
callback in class
'''
class A:
	def __init__(self, cb:func(int)(int), x:int, y:int, z:int=1):
		int self.x = x
		int self.y = y
		int self.z = z
		func(int)(int) self.callback = cb

	def call(self, a:int ) -> int:
		return self.callback( a + self.x + self.y + self.z )

def mycb( x:int ) ->int:
	return x + 1000

def main():
	a = A(
		mycb, 
		100, 
		200, 
		z=300
	)
	#print( a.x )
	#print( a.y )
	#print( a.z )

	TestError( a.call(-600)==1000 )

