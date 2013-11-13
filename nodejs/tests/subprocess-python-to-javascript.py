from nodejs.os import *
from nodejs.io import *
from nodejs.subprocess import *

vm = require('vm')


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
	path = '/tmp/input1.py'
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
	path = '/tmp/input2.py'
	open( path, 'w' ).write( src )
	args = [
		os.path.join( PATHS['pythonjs'], 'pythonjs.py'),
		path
	]
	p = subprocess.call('python2', args, callback=callback )


print 'testing pythonjs_to_javascript'
pythonjs_to_javascript( source, show_result )


def python_to_javascript(source, callback):
	func = lambda data: pythonjs_to_javascript(data, callback)
	python_to_pythonjs( source, func )


## for some reason this failed because calling gets broken:
## if (args instanceof Array && {}.toString.call(kwargs) === '[object Object]' && arguments.length == 2)
## something above was not working, we do not need this anyways because this was a workaround
## to try to get `eval` to work, NodeJS is picky about `var` because of how modules are loaded,
## something without var is considered global, and becomes part of the context that eval will use.
#def _eval(source):
#	vm.runInContext( source, pythonjs )
#	print 'eval finished'

def pyexec( source ):
	python_to_javascript( source, eval )


setTimeout(
	lambda : pyexec( "print 'hello world'"),
	1000
)

test = """
print 'testing class A'
class A:
	def __init__(self, x,y,z):
		print x,y,z
		self.x = x
		self.y = y
		self.z = z

	def foo(self, a,b,c):
		print 'a', a
		print 'b', b
		print self.x
		print self.y
		return self.x + self.y + self.z

	def bar(self):
		return self.x * self.y * self.z

a = A( 100, 200, 300 )
print 'A instance created'
print a.foo()
print a.bar()

"""

setTimeout(
	lambda : python_to_javascript( test, show_result ),
	4000
)

setTimeout(
	lambda : pyexec(test),
	6000
)

