"""sprintf"""
from runtime import *

def main():
	a = '%s.%s' %('X', 'Y')
	assert(a[0] == 'X')
	assert(a[1] == '.')
	assert(a[2] == 'Y')

	b = 'X%sX' %1.1
	assert(b == 'X1.1X')

main()