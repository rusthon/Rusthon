"""if not"""

def main():
	a = False
	b = False
	if not a:
		b = True

	TestError( b == True )

	a = 0
	b = False
	if not a:
		b = True

	TestError( b == True )

	a = 0.0
	b = False
	if not a:
		b = True

	TestError( b == True )

	a = None
	b = False
	if not a:
		b = True

	TestError( b == True )
