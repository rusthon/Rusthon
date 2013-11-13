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


def python_to_pythonjs( src, callback ):
	path = '/tmp/input.py'
	open( path, 'w' ).write( src )
	args = [
		os.path.join( PATHS['pythonjs'], 'python_to_pythonjs.py'),
		path
	]
	p = subprocess.call('python2', args, callback=callback )


source = 'def test(): print("hello world")'
print 'testing python_to_pythonjs'
python_to_pythonjs( source, show_result )


def pythonjs_to_javascript( src, callback ):
	path = '/tmp/input.py'
	open( path, 'w' ).write( src )
	args = [
		os.path.join( PATHS['pythonjs'], 'pythonjs.py'),
		path
	]
	p = subprocess.call('python2', args, callback=callback )


print 'testing pythonjs_to_javascript'
pythonjs_to_javascript( source, show_result )

