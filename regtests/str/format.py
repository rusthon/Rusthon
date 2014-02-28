"""string.format"""

def main():
	a = '{x}{y}'.format( x='A', y='B')
	TestError(a == 'AB')
