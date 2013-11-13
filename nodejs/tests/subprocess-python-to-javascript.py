from nodejs.os import *
from nodejs.io import *
from nodejs.subprocess import *

PATHS = dict(
	pythonjs = os.path.abspath('pythonjs'),
	nodejs_bindings = os.path.abspath('nodejs/bindings'),
	runtime = os.path.abspath('pythonjs.js'),
)

print PATHS['pythonjs']
print PATHS['nodejs_bindings']
print PATHS['runtime']

def show_result( data ):
	print '-------- translation -----------'
	print data


def python_to_pythonjs( src ):
	f = open( '/tmp/test.py', 'w' )
	f.write( src )

	args = [
		os.path.join( PATHS['pythonjs'], 'python_to_pythonjs.py'),
		'/tmp/test.py'
	]
	p = subprocess.call('python2', args, callback=show_result )



source = 'def test(): print("hello world")'
print 'testing python_to_pythonjs'
python_to_pythonjs( source )



