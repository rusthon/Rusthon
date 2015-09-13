from runtime import *
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
	assert( f(1,2) == 3 )

	assert( (lambda a,b: a+b)(1,2) == 3 )

	assert( get_lambda()(1,2) == 3 )

	funcs = get_lambdas()
	assert( funcs[0](1,2) == 3 )
	assert( funcs[1](1,2) == 3 )

	funcs = [lambda a,b: a+b, lambda x,y: x+y]
	assert( funcs[0](1,2) == 3 )
	assert( funcs[1](1,2) == 3 )

	d = { 'x':lambda a,b: a+b }
	assert( d['x'](1,2) == 3 )

	e = ( lambda a,b: a+b, lambda x,y: x+y )
	assert( e[0](1,2) == 3 )
	assert( e[1](1,2) == 3 )

	r = call_lambda( lambda : int(100) )
	assert( r==100 )


	r = call_lambda2( callback = lambda : int(200) )
	assert( r==200 )
main()
