"""catch KeyError"""

def main():
	D = {}
	a = False
	try:
		a = D['XXX']
	except KeyError:
		a = True

	TestError( a == True )
