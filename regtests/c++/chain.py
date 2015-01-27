'''
chain
'''

class A:
	def __init__(self):
		let self.val : float = 0
	def add(self, a:float) ->self:
		self.val += a
		return self
	def mult(self, a:float) ->self:
		self.val *= a
		return self
	def div(self, a:float) ->self:
		self.val /= a
		return self


def main():
	a = A()
	val = a.add(100.0).mult(3.0).div(2.0).val
	print(val)
