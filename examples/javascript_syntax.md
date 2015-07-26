testing
-------

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_syntax.md
```

html
----


@index.html
```html
<html>
<head>

<@myscript>

</head>
<body>
<button onclick="javascript:hello_world()">clickme</button>

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

## the runtime provides some fake python libs ##
J = json.loads( '{"x":1}' )  
print  J 

s1 = set( [1,2,3,1,2])
print s1
s2 = frozenset( [0,1,1,1,1,20])
print s2
s3 = s1.difference(s2)
print s3

class Channel():
	def send(self,ob):
		print 'sending:' + ob
		return ob

chan = Channel()
with mymacro as "chan.send(JSON.stringify(%s))":
	mymacro( s3 )

print 'chan is an isinstance of Channel'
print isinstance(chan, Channel)  ## True
print isinstance(chan, Array)    ## False

with webworker:
	class Worker():
		def send(self,ob):
			print 'sending:' + ob
			return ob


def hello_world():
	window.alert(" new hi R arrow -> and L arrow <- and $ $. $(")


X = []
Z = None

def test():
	global X, Z
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

	class Root:
		def root(self):
			return 'hi from root'

	class Nested:
		class SubClass(Root):
			def foo(self):
				print 'calling Nested.Subclass.foo'
				print Nested
				print Nested.SubClass
				print 'Nested.Subclass: foo OK'
				return new(Nested.SubClass())

		def foobar(self, x):
			print x

			class SubNested:
				def submeth(self, x,y):
					print x+y

			snest = SubNested()
			snest.submeth('testing sub', 'NESTED')
			return snest


	nest = Nested()
	snest = nest.foobar('testing nexted class')
	print snest
	snest.submeth('called from outer scope','subnested')

	scls = new Nested.SubClass()
	scls2 = scls.foo()

	print 'TESTING META STUFF'
	print scls.__class__
	print scls.__class__.__name__
	print 'testing isinstance'
	print isinstance(scls, Nested.SubClass)
	print isinstance(scls, scls.__class__)

	class SubSubClass(Nested.SubClass):
		def bar(self):
			print 'SubSubClass.bar OK'

	print 'testing issubclass'
	print issubclass(SubSubClass, Nested.SubClass)
	print issubclass(Nested.SubClass, Root)
	print issubclass(SubSubClass, Root)
	print 'testing SubSubClass...'
	ssc = SubSubClass()
	ssc.foo()
	ssc.bar()

	print "STRING TESTS"
	print 'a b c'.split()
	print 'axbxc'.replace('x', 'Z')

	print dir(X)

	print 'testing isdigit'
	print '1'.isdigit()
	print 'A'.isdigit()
	print len('123')

	test_spawn()


def test_spawn():
	## in c++ becomes std::thread lambda wrapped
	## here in js it becomes `worker1 = __workerpool__.spawn({'call|new':'Channel', 'args':[]})
	print 'spawn workers'
	worker1 = spawn(
		Worker(),
		cpu = 0
	)
	worker2 = spawn(
		Worker(),
		cpu = 1
	)
	window.setTimeout(
		lambda: test_workers(worker1,worker2),
		1500,
	)

def test_workers(worker1, worker2):
	## in c++ this becomes worker1.send(msg)
	## here in js it becomes __workerpool__.postMessage([worker.__workerid__, msg])
	print 'sending data to workers'
	worker1 <- 'msg 1'
	worker1 <- 'msg 2'
	worker1 <- 'msg 3'
	worker1 <- 'msg 4'

	worker2 <- 'msg 5'
	worker2 <- 'msg 6'
	worker2 <- 'msg 7'
	worker2 <- 'msg 8'

	## in c++ becomes worker1.recv()
	## here it becomes a new callback that passes res1
	## `__workerpool__.recv(worker.__workerid__, function(res1) { ...rest of function body...}
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



window.setTimeout(test, 1000)

```
