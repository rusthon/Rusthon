"""string iteration requires wrappingn with `iter(my)`"""
from runtime import *

def main():
	a = list("abc")
	print a
	assert(a[0] == 'a')
	assert(a[1] == 'b')
	assert(a[2] == 'c')
	print '--------'
	b = ['a']
	for chr in iter("xyz"):
		print chr
		b.append(chr)
		print b
	print '--------'
	print b
	assert(b[0] == 'a')
	assert(b[1] == 'x')
	assert(b[2] == 'y')
	assert(b[3] == 'z')

	b = ['a']
	mystr = "xyz"
	for char in iter(mystr):
		print char
		b.append(char)
		print b
	print '--------'
	print b
	assert(b[0] == 'a')
	assert(b[1] == 'x')
	assert(b[2] == 'y')
	assert(b[3] == 'z')

	x = []
	y = [1,2,3]
	## should be faster to call iter(myarr) when myarry is short. 
	## for long arrays use `for v in myarry`
	for v in iter(y):
		x.append(v)
		print v
		print x
	print '--'
	print x

main()