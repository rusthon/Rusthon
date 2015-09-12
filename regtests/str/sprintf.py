"""sprintf"""
from runtime import *

def main():
	a = '%s.%s' %('X', 'Y')
	assert(a[0] == 'X')
	assert(a[1] == '.')
	assert(a[2] == 'Y')

	b = 'X%sX' %1.1
	assert(b == 'X1.1X')

main()123456
vr unithon-flowspace, ace.js rust servo user custom debugger+docker.