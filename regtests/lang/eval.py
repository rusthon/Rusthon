'''
eval
'''

def foo(): return 42
bar = lambda: 42

def main():
	eval('a = bar()') # This one works
	eval('b = foo()') # 'foo' is undefined in normal mode under NodeJS but works in NodeWebkit and Chrome!?
	TestError( a==42 )
	TestError( b==42 )
