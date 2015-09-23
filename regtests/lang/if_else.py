from runtime import *
'''
if/else
'''

#def func(x=None, callback=None):
def func(x=False, callback=None ):
	a = False
	if x:   ## can c++ templates support this pythonic style?
		a = False
	else:
		a = True

	assert( a==True )

	a = False
	if callback:
		a = True
	else:
		a = False
	assert( a==True )

def main():
	a = False
	if 1:
		a = True
	assert( a==True )

	a = False
	if False:
		a = False
	else:
		a = True

	assert( a==True )

	a = False
	if None:
		a = False
	else:
		a = True

	assert( a==True )

	def cb() ->int:
		return 1+1

	func( callback=cb )



main()
