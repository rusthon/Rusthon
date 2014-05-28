"""if x in list"""
def main():
	a = ['foo', 'bar']
	TestError( 'foo' in a )

	b = [0, 1, 2]
	TestError( 2 in b )
