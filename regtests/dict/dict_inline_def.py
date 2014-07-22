"""dict inline def"""


def main():

	d = { 'callback': def (x,y):
		return x+y
	}
	TestError( d['callback'](1,2) == 3 )

