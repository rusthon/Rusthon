from runtime import *
"""dict.keys() and iter"""

def main():
	a = {'foo':'bar'}
	keys = a.keys()
	assert( 'foo' in keys )

	print 'testing iter over dict'
	## this is not allowed, a must be wrapped with `iter(a)`
	#for key in a:
	print a
	for key in iter(a):
		print key
		print a[key]

main()
