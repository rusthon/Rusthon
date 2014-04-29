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

	TestError( err1 == 0 )
	TestError( err2 == 0 )
	TestError( err3 == 0 )

	a = A()
	a.x = []
	if a.x:
		err4 = 1
	else:
		err4 = 0

	TestError( err4 == 0 )
