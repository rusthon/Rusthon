'''
if/else
'''

#def func(x=None, callback=None):
def func(x:bool=False, callback:lambda()(int)=None ):
	a = False
	if x:   ## can c++ templates support this pythonic style?
		a = False
	else:
		a = True

	TestError( a==True )

	a = False
	if callback:
		a = True
	else:
		a = False
	TestError( a==True )

def main():
	a = False
	if 1:
		a = True
	TestError( a==True )

	a = False
	if False:
		a = False
	else:
		a = True

	TestError( a==True )

	a = False
	if None:
		a = False
	else:
		a = True

	TestError( a==True )

	cb = lambda : 1+1
	func( callback=cb )


