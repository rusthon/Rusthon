'''
delete pointer
'''
class A:
	def __init__(self, x:int ):
		self.x = x
	def __del__(self):
		print( 'goodbye')

def main():
	a = A()
	print a
	del a
	print 'done'
