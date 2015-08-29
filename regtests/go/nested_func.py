'''
lambda func
'''

def main():
	def F(x:int) ->int:
		return x*2

	a = F(10)
	print a
	assert a==20
