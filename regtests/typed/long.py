"""long static type"""

def main():
	long x = 65536
	long y = x * x
	long z = 4294967296
	TestError( y==z )

	long a = z + z
	long b = 8589934592
	TestError( a==b )

	TestError( y < b )
	TestError( b > y )

	TestError( y <= b )
	TestError( b >= y )

## TODO check why this fails when used with translator.py directly (bad indent bug)