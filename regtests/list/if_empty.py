from runtime import *
"""if empty list then false"""

class A:
	pass

def main():
	d = []
	#if d:  ## this is not allowed, and will raise an error at runtime
	if len(d):
		err1 = 1
	else:
		err1 = 0

	if len([]):
		err2 = 1
	else:
		err2 = 0

	d.append('xxx')
	if len(d):
		err3 = 0
	else:
		err3 = 1

	assert( err1 == 0 )
	assert( err2 == 0 )
	assert( err3 == 0 )

	a = A()
	ok = False
	#if a:  ## this is not allowed, and will raise an error at runtime
	if a is not None:
		ok = True
	assert ok

	a.x = []
	if len(a.x):
		err4 = 1
	else:
		err4 = 0

	assert( err4 == 0 )

main()
