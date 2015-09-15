from runtime import *
"""list multiplication"""


def main():
	a = ['hi']
	print a
	with operator_overloading:
		b = a * 2
	assert( len(b)==2 )
	assert( b[0]=='hi' )
	assert( b[1]=='hi' )
	print b

main()
