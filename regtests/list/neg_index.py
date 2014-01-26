"""negative list indices"""
def main():
	a = [1,2,3,4]
	idx = -2
	TestError( a[-1]==4 )  ## this works in javascript mode because the translator knows index is negative
	TestError( a[idx]==3 ) ## this fails in javascript mode.
