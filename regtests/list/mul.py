"""list multiplication"""


def main():
	a = ['hi']
	b = a * 2
	TestError( len(b)==2 )
	TestError( b[0]=='hi' )
	TestError( b[1]=='hi' )
