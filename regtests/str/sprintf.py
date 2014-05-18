"""sprintf"""

def main():
	a = '%s.%s' %('X', 'Y')
	TestError(a[0] == 'X')
	TestError(a[1] == '.')
	TestError(a[2] == 'Y')

	b = 'X%sX' %1.1
	TestError(b == 'X1.1X' or b == 'X1.100000X')
