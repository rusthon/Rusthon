from runtime import *
"""if not"""

def main():
	a = False
	b = False
	if not a:
		b = True

	assert( b == True )

	a = 0
	b = False
	if not a:
		b = True

	assert( b == True )

	a = 0.0
	b = False
	if not a:
		b = True

	assert( b == True )

	a = None
	b = False
	if not a:
		b = True

	assert( b == True )

main()
