"""keywords"""
def f(a, b=None, c=None):
	return (a+b) * c

def f2(**kw):
	a = 0
	for key in kw:
		a += kw[key]
	return a

def main():
	TestError( f(1, b=2, c=3) == 9)  ## inorder works in javascript mode
	TestError( f(1, c=3, b=2) == 9)  ## out of order fails in javascript mode

	TestError( f2(x=1,y=2) == 3 )