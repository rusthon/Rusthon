'''
return a class instance
'''
with pointers:
	class A:
		def __init__(self, x:int, y:int):
			self.x = x
			self.y = y

	def create_A() -> A:
		#a = A(1,2)  ## not valid because `a` gets free`ed when function exists
		a = new A(1,2)  ## using `new` the user must manually free the object later
		return a

	def main():
		x = create_A()
		print(x)
		print(x.x)
		print(x.y)
