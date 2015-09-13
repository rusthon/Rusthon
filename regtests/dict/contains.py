from runtime import *
"""key in dict"""

def main():
	## mixing string keys and number keys in a dict literal
	## is allowed in python, but not in Rusthon
	#a = {'2': 22, 3:33}
	#assert( '2' in a )
	#assert( 3 in a )

	a = {2: 22, 3:33}
	assert( 2 in a )
	assert( 3 in a )


main()
