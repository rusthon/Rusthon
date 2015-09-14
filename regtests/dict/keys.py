from runtime import *
"""dict.keys()"""

def main():
	a = {'foo':'bar'}
	keys = a.keys()
	assert( 'foo' in keys )

main()
