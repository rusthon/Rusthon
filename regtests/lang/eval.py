from runtime import *
'''
eval
'''

def foo(): return 42
bar = lambda: 42

def main():
	eval('a = bar()') # This one works
	eval('b = foo()') # 'foo' is undefined in normal mode under NodeJS but works in NodeWebkit and Chrome!?
	assert( a==42 )
	assert( b==42 )

main()
