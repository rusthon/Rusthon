"""variable keywords"""

def f2(**kw):
	a = 0
	for key in kw:
		a += kw[key]
	return a

def main():

	TestError( f2(x=1,y=2) == 3 )