JavaScript Backend - Basics
-------

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_syntax.md
```

See Also
--------
* [hello_javascript.md](hello_javascript.md)
* [javascript_classes.md](javascript_classes.md)
* [hello_threejs.md](hello_threejs.md)
* [javascript_static_types.md](javascript_static_types.md)



html
----


@index.html
```html
<html>
<head>
</head>
<body>
<button onclick="javascript:hello_world()">clickme</button>
<@myscript>
</body>
</html>
```


rusthon javascript backend
--------------------------

Below `@myscript` is given on the line just before the fenced rusthon code block.  This allows you to insert multiple scripts into your html, in the head or body.

The extra syntax `switch` and `default` is also supported.

@myscript
```rusthon
#backend:javascript
from runtime import *


class MyChannel():
	def send(self,ob):
		print 'calling MyChannel.send:' + ob
		return ob
	def keys(self):
		return 420


with webworker:
	class Worker():
		def send(self,ob):
			print 'sending:' + ob
			return ob


def mydecorator( f ):
	f.something = 'decorators ok'
	return f

@mydecorator
def hello_world():
	window.alert(" new hi R arrow -> and L arrow <- and $ $. $(")

assert hello_world is not undefined
print hello_world.something

X = []
Z = None

@debugger
def test():
	global X, Z

	mystring1 = "hello %s" %"world"
	print mystring1

	mystring2 = "%s %s" %("hello", "world")
	print mystring2

	## the runtime provides some fake python libs ##
	J = json.loads( '{"x":1}' )  
	print  J 

	s1 = set( [1,2,3,1,2])
	print s1
	s2 = frozenset( [0,1,1,1,1,20])
	print s2
	s3 = s1.difference(s2)
	print s3

	chan = MyChannel()

	## macros let you inline javascript and compress multiple things into one simple macro function
	with mymacro as "chan.send(JSON.stringify(%s)); console.log('macro test OK');":
		mymacro( s3 )

	print 'chan is an isinstance of MyChannel'
	print isinstance(chan, MyChannel)  ## True
	print isinstance(chan, Array)    ## False

	mydict = {keys:1}
	assert mydict[ 'keys' ] == 1
	print mydict.keys()

	print chan.keys()
	assert chan.keys() == 420

	#copy = dict(mydict)

	## this is a very rare case, but it still works ##
	def f():
		return 'VERYRARE'
	mydict2 = {keys: f}
	assert mydict2['keys']() == 'VERYRARE'
	assert mydict2.keys()    != 'VERYRARE'

	## the key type of this dict can be determined at translation time as int
	idict = {0:'a', 1:'b', 2:'c'}

	## this returns an array of ints ##
	print idict.keys()
	for k in idict.keys():
		assert isinstance(k, int)

	## having numbers as keys allows you to use `max()` as you normally would in python
	assert max( idict.keys() ) == 2

	## this also restores `k` to type int from the hash keys ##
	for k in idict:
		assert isinstance(k, int)

	## the hash keys are still actually strings and it needs
	## to be this way to stay compatible with external js.
	assert idict['0'] == 'a'

	a = 1
	b = 2
	if a <= b-1:
		print 'ok'
	else:
		print 'error'

	switch a:
		case 0:
			print 'no'
		case 1:
			print 'yes'
			print 'switch syntax ok'

	switch b:
		case 0:
			print 'error'
		case 1 or 10:
			print 'error'
		default:
			print 'switch default ok'

	## get translated to the ternary operator in `test?truevalue:falsevalue`
	print 'testing ternary'
	tertest = a if True else b
	assert tertest==1
	print 'ternay OK'

	with operator_overloading:
		X = [1,2]
		arr = [3,4]
		X += arr

	## `oo` is an alias for `operator_overloading`
	with oo:
		Z = [10,20] + [30,40]


	print X
	print Z
	print X.pop()

	for i,e in enumerate(X):
		print i, e

	print 'X is list:', isinstance(Z, list)
	print 'X is really a js Array:', isinstance(Z, Array)

	try:
		getattr(X, 'notthere')  ## throws exception
	except AttributeError:
		print 'caught attribute error OK'

	#getattr(X, 'notthere')  ## throws exception


	print "STRING TESTS"
	print 'a b c'.split()
	print 'axbxc'.replace('x', 'Z')

	print dir(X)

	print 'testing isdigit'
	print '1'.isdigit()
	print 'A'.isdigit()
	print len('123')

	## jquery or some external library that uses `$` ##
	def $(w):
		print(w)
	$.bla = $

	if $ is not undefined:
		$('testing calling $')
		$.bla('testing bla')
		$($)
		$ = 1
	else:
		print 'missing jquery'

	test_spawn()


def test_spawn():
	print 'spawn workers'
	worker1 = spawn(
		Worker(),
	)
	worker2 = spawn(
		Worker(),
	)
	window.setTimeout(
		lambda: test_workers(worker1,worker2),
		1500,
	)

def test_workers(worker1, worker2):
	print 'sending data to workers'
	worker1 <- 'msg 1'
	worker1 <- 'msg 2'
	worker1 <- 'msg 3'
	worker1 <- 'msg 4'

	worker2 <- 'msg 5'
	worker2 <- 'msg 6'
	worker2 <- 'msg 7'
	worker2 <- 'msg 8'

	print 'getting data from workers'
	res = <- worker1
	print res
	res = <- worker1
	print res
	res = <- worker1
	print res
	res = <- worker1
	print res

	res = <- worker2
	print res
	res = <- worker2
	print res
	res = <- worker2
	print res
	res = <- worker2
	print res

	#worker1.terminate()  ## TODO



test()

```
