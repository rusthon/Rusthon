"""dict.keys()"""

def main():
	a = {'foo':'bar'}
	keys = a.keys()
	TestError( 'foo' in keys )
