Webworker Syntax
--------------------------

https://github.com/rusthon/Rusthon/wiki/WebWorker-Syntax

testing
-------

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_webworkers_advanced.md
```

html
----


@index.html
```html
<html>
<head>


</head>
<body>
<pre id="CONTAINER">
</pre>
<@myscript>
</body>
</html>
```

Example
--------------------------

The class `WorkerX` defines a `send` method that takes a message and returns something to the main thread.
Spawn is used to create two instances of `WorkerX`, these become the channels for passing data and messages.

The control loop `select:` allows you to select from multiple channels at once for reading data, 
this syntax is inspired by the Golang [select statement](http://golangtutorials.blogspot.com/2011/06/channels-in-go-range-and-select.html)

Methods and attributes can be accessed on the channel by copying the data into the main thread,
this is done with `a = <- worker.somemethod()` for methods and `a = <- worker.x` for attributes.

Functions declared inside the webworker can be called from the main thread by: `a = <- somefunction()`

Channel objects (any class defined in the webworker and spawned from the main thread) can also send data
back to the main thread using: `self <- message`.  The main thread can receive these messages inside a select loop,
or simply by getting the next message off the queue with the blocking assignment syntax: `message = <- channel`.

@myscript
```rusthon
#backend:javascript
from runtime import *

def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)

with webworker:

	def somefunc( a, b ):
		return 'hello' + a + b

	def CalcFib(n):
		if n == 0: return 0
		elif n == 1: return 1
		else: return CalcFib(n-1)+CalcFib(n-2)


	class WorkerX():
		def __init__(self, x,y,z):
			self.x = x
			self.y = y
			self.z = z
			setTimeout( self.dowork.bind(this), 1000 )

		def send(self, x=None, y=None, z=None):
			self.x += x
			self.y += y
			self.z += z
			return self.getsum()

		def getsum(self):
			return self.x + self.y + self.z

		def mymethod(self, a,b,c):
			print 'calling mymethod'
			return a*b*c

		def dowork(self):
			print 'webworker doing work'
			for i in range(32):
				print 'calc fib degree:'+i
				self <- CalcFib(i)

@debugger
def test():
	## testing multiple cores ##
	show('spawn workers')
	worker1 = spawn(
		WorkerX(1,1,1),
		cpu = 1
	)
	a = 100
	worker2 = spawn(
		WorkerX(a,a,a),
		cpu = 2
	)

	print worker1
	print worker2
	## wait for awhile before sending messages ##
	window.setTimeout(
		lambda: test_workers(worker1,worker2),
		2000,
	)

def test_workers(worker1, worker2):
	show('testing simple call')
	#if worker1.is_busy():
	#	raise RuntimeError('got busy')

	for i in range(64):
		print 'trying to select on workers'
		select:
			case res = <- worker1:
				show('case-worker1:' + res)
			case res = <- worker2:
				show('case-worker2:' + res)


	## TODO: need to rethink how this works
	## because somefunc could be returning some important state,
	## and with multiple workers on multiple cores, there are different states now.
	## could be something like this: `res = <- worker1::somefunc( 'foo', 'bar' )`
	## but that is ugly and in that case the user could have simply made a wrapper method to call the function.
	## another options is this: `res = <- somefunc[ CPUID ]('foo', 'bar')` - this makes more sense.
	#res = <- somefunc( 'foo', 'bar' )
	#show('somefunc:' + res)


	show('getting data from workers')

	res = <- worker1.mymethod(10, 10, 2)
	show( 'worker1.mymethod:' + res)

	res = <- worker1.x
	show('worker1.x:' + res)
	res = <- worker1.y
	show('worker1.y:' + res)
	res = <- worker1.z
	show('worker1.z:' + res)

	show('worker2')
	res = <- worker2.getsum()
	show( 'worker2.getsum:' + res)
	res = <- worker2.x
	show('worker2.x:' + res)
	res = <- worker2.y
	show('worker2.y:' + res)
	res = <- worker2.z
	show('worker2.z:' + res)

	show('sending data to workers')
	msg = {
		'x':1, 
		'y':2,
		'z':3
	}

	for i in range(10):
		worker1 <- msg
		worker2 <- msg

	sleep(1.0)

	for i in range(20):
		print 'trying to select on workers'
		select:
			case res = <- worker1:
				show('case-worker1:' + res)
			case res = <- worker2:
				show('case-worker2:' + res)

	#res = <- worker2
	#show(res)
	#res = <- worker2
	#show(res)
	#res = <- worker2
	#show(res)
	#res = <- worker2
	#show(res)



window.setTimeout(test, 1000)

```
