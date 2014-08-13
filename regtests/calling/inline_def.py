"""inline def"""

def test( callback1=None, callback2=None ):
	return {'cb1': callback1, 'cb2': callback2 }

def main():
	o = test( callback1=def (x,y):
		return x+y,
		callback2 = def (x):
			return x*2
	)
	TestError( o['cb1'](1,2) == 3 )
	TestError( o['cb2'](100) == 200 )

