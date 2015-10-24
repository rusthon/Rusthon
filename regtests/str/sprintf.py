"""sprintf"""
from runtime import *

def main():
	a = '%s.%s' %('X', 'Y')
	print a
	assert(a[0] == 'X')
	assert(a[1] == '.')
	assert(a[2] == 'Y')

	b = 'X%sX' %1.1
	print b
	assert(b == 'X1.1X')

	c = 'foo%s %s' %(1*1, 2+2)
	print c

main()