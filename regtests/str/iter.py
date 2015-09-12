"""The string iterator"""
from runtime import *

def main():
	a = list("abc")
	assert(a[0] == 'a')
	assert(a[1] == 'b')
	assert(a[2] == 'c')

	b = ['a']
	for i in "xyz":
		b.append(i)
	assert(b[0] == 'a')
	assert(b[1] == 'x')
	assert(b[2] == 'y')
	assert(b[3] == 'z')

main()