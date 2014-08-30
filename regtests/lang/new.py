'''
js new keyword
'''

def main():
	#a = new Date()  ## this also works
	a = JS(' new Date()')
	TestError( a.getFullYear()==2014 )
