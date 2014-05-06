"""Function call with the name of a parameter without default value"""
def f1(a):
	return a

def f2(a=1):
	return a

def main():
	TestError( f2( 100 ) == 100 )

	TestError( f1( a=100 ) == 100 )
