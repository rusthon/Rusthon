"""replace"""

def main():
	a = 'abc'
	b = a.replace('a', 'A')
	TestError( b == 'Abc')

	a = 'aaa'
	b = a.replace('a', 'A')
	TestError( b == 'AAA')
