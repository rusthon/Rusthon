"""catch AttributeError"""

class A: pass

def main():
	a = A()
	b = False
	try:
		b = a.xxx
	except AttributeError:
		b = True

	TestError( b == True )
