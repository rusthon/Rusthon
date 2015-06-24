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

Webworker Syntax
--------------------------

The Javascript backend uses some syntax inspired by Golang to simplify using WebSockets.
Below the class `Worker` must define a `send` method that takes a message and returns something to the main thread.

@myscript
```rusthon
#backend:javascript
from runtime import *

def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)

with webworker:

	def somefunc():
		return 'hello'

	class Worker():
		def __init__(self, x,y,z):
			self.x = x
			self.y = y
			self.z = z

		def send(self, x=None, y=None, z=None):
			self.x += x
			self.y += y
			self.z += z

		def getsum(self):
			return self.x + self.y + self.z

def fixme(): pass

def test():
	show('spawn workers')
	worker1 = spawn(
		Worker(1,1,1)
	)
	a = 100
	worker2 = spawn(
		Worker(a,a,a)
	)
	## wait for awhile before sending messages ##
	window.setTimeout(
		lambda: test_workers(worker1,worker2),
		1500,
	)

def test_workers(worker1, worker2):
	show('testing simple call')
	res = <- somefunc()

	show('sending data to workers')
	msg = {
		'x':1, 
		'y':2,
		'z':3
	}

	for i in range(10):
		worker1 <- msg

	show('getting data from workers')
	res = <- worker1.getsum()
	show(res)
	res = <- worker1.x
	show(res)
	res = <- worker1.y
	show(res)
	res = <- worker1.z
	show(res)

	res = <- worker2
	show(res)
	res = <- worker2
	show(res)
	res = <- worker2
	show(res)
	res = <- worker2
	show(res)



window.setTimeout(test, 1000)

```
