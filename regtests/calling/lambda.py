"""lambda function"""

def get_lambda():
	return lambda x,y: x+y

def get_lambdas():
	return [lambda a,b: a+b, lambda x,y: x+y]

def call_lambda( F ):
	return F()

def call_lambda2( callback=None ):
	return callback()

def main():
	f = lambda a,b: a+b
	TestError( f(1,2) == 3 )

	TestError( (lambda a,b: a+b)(1,2) == 3 )

	TestError( get_lambda()(1,2) == 3 )

	funcs = get_lambdas()
	TestError( funcs[0](1,2) == 3 )
	TestError( funcs[1](1,2) == 3 )

	funcs = [lambda a,b: a+b, lambda x,y: x+y]
	TestError( funcs[0](1,2) == 3 )
	TestError( funcs[1](1,2) == 3 )

	d = { 'x':lambda a,b: a+b }
	TestError( d['x'](1,2) == 3 )

	e = ( lambda a,b: a+b, lambda x,y: x+y )
	TestError( e[0](1,2) == 3 )
	TestError( e[1](1,2) == 3 )

	r = call_lambda( lambda : int(100) )
	TestError( r==100 )


	r = call_lambda2( callback = lambda : int(200) )
	TestError( r==200 )