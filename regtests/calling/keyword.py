"""keywords"""
def f(a, b=None, c=None):
	return (a+b) * c


def main():
	TestError( f(1, b=2, c=3) == 9)  ## inorder works in javascript mode
	TestError( f(1, c=3, b=2) == 9)  ## out of order fails in javascript mode
