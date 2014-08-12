'''
simple class
'''
class A:
	{
		x:int,
		y:int,
		z:int,
	}
	def __init__(self, x:int, y:int, z:int=1):
		self.x = x
		self.y = y
		self.z = z

def main():
	a = A( 100, 200, z=9999 )
	print( a.x )
	print( a.y )
	print( a.z )