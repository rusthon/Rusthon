"""lambda function"""

def get_lambda():
	return lambda x,y: x+y

def main():
	f = lambda a,b: a+b
	TestError( f(1,2) == 3 )

	TestError( (lambda a,b: a+b)(1,2) == 3 )

	TestError( get_lambda()(1,2) == 3 )
