"""hello world"""

XXX = 'myglobal'  ## this is a static string

def myprint( a:string, b:string ):
	print a + b


def main():
	print "hi"
	myprint('hello ', 'world')

	## TODO - should this automatically be converted from a static string to a String with `String.from_str()`
	myprint('hi ', str(XXX) )