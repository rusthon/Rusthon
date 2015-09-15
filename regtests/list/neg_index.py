from runtime import *
"""negative list indices"""
def main():
	a = [1,2,3,4]
	## negative indices are allowed when using a number literal as the index,
	## this is the most common use case, because often you want to index from
	## the end with a literal number and not a variable.
	assert( a[-1]==4 )
	assert a[-2]==3
	assert a[-3]==2
	assert a[-4]==1

	## this is allowed in regular python, but not in rusthon.
	idx = -2
	#assert( a[idx]==3 )
	## if you really need to use a variable to perform a negative index,
	## this is the workaround.
	assert a[a.length+idx-1]

main()
