'''
keyword arguments
'''

def f1( a=1 ) -> int:
	return a*2

## this break rust because the global kwargs-type then requires `b` and `__use__b`
## but the caller only gives `a` and `__use__a`
def f2( a=1, b=2 ) -> int:
	return a + b

def main():
	print( f1(a=100) )
	#print( f2(a=100, b=200) )  ## TODO fix in c++
