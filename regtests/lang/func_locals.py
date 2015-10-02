from runtime import *
'''
inspect locals of a function at runtime for debugging
'''

@locals
def myfunc(value='bar'):
	x = 1
	y = {foo:value}
	@locals
	def nested():
		z = 'FOO'
		return value + 'NESTED'

	return nested()

def main():
	print myfunc.locals
	print myfunc()
	print myfunc.locals
	assert myfunc.locals.x == 1
	assert myfunc.locals.y.foo=='bar'
	myfunc(value='X')
	print myfunc.locals
	assert myfunc.locals.y.foo=='X'

	print myfunc.locals.nested.locals.z
	assert myfunc.locals.nested.locals.z=='FOO'

main()
