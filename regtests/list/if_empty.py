from runtime import *
"""if empty list then false"""

class A:
	pass

def main():
	d = []
	if d:
		err1 = 1
	else:
		err1 = 0

	if []:
		err2 = 1
	else:
		err2 = 0

	d.append('xxx')
	if d:
		err3 = 0
	else:
		err3 = 1

	assert( err1 == 0 )
	assert( err2 == 0 )
	assert( err3 == 0 )

	a = A()
	a.x = []
	if a.x:
		err4 = 1
	else:
		err4 = 0

	assert( err4 == 0 )

main()
