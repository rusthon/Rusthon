```rusthon

class A:
	'''
	doc about my class
	'''
	def mymethod(self):
		'''
		doc about mymethod
		'''
		pass

def somefunc( x:int ) -> bool:
	'''
	my documentation on somefunc
	@param [in] x  Number to print.
 	@retval TRUE   Returns true if less than ten.
 	@retval FALSE  Returns false otherwise.
	'''
	print(x)
	if x < 10: return True
	else: return False

def main():
	somefunc( 10 )
```

