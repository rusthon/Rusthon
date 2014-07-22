"""dict inline def"""


def main():

	d = { 'callback': def (x,y):
		return x+y
	}
	TestError( d['callback'](1,2) == 3 )

	a = { 'cb1': def (x,y):
		return x+y,
		'cb2' : def (x):
			return x*2
	}
	TestError( a['cb1'](1,2) == 3 )
	TestError( a['cb2'](100) == 200 )
