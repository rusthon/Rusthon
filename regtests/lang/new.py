from runtime import *
'''
js new keyword
'''

def main():
	## new as keyword can be used in simple statements, but can break the parser in some cases,
	## it is only allowed to make it easy to copy and paste js code and convert it to rusthon.
	a = new Date()
	b = new( Date() )  ## using new as a function call is safer and always works
	assert( a.getFullYear()==2015 )
	assert( b.getFullYear()==2015 )

main()
