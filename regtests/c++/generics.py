'''
generic functions
'''

def myfunc( x:int ):
	print( x * 100 )

def myfunc( x:string ):
	print( x + 'world' )

def main():
	myfunc( 10 )
	myfunc( 'hello' )
