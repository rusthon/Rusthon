"""lambda function"""

def main():
	f = lambda a,b: a+b
	TestError( f(1,2) == 3 )

