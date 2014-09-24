'''
map comprehensions
'''

def main():
	m = map[int]string{ a:'xxx' for a in range(10)}
	TestError( m[0]=='xxx' )
	TestError( m[9]=='xxx' )
