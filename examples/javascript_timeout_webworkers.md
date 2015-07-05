testing
-------

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_timeout.md
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

Timeout Syntax
--------------------------
`with timeout( ms ):`, where `ms` is the number of milliseconds allowed to try to finish the block.

note the use of the builtin `sleep(0.5)`, this pauses the main thread for half a second, so the webworker has time
to process the input events and fill up its output message queue.

@myscript
```rusthon
#backend:javascript
from runtime import *

def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)


with webworker:

	class WorkerX():
		def __init__(self, x,y,z):
			self.x = x
			self.y = y
			self.z = z

		def send(self, x=None, y=None, z=None):
			self.x += x
			self.y += y
			self.z += z
			return self.getsum()

		def getsum(self):
			return self.x + self.y + self.z



def test():
	show('spawn workers')
	worker1 = spawn(
		WorkerX(1,1,1)
	)
	a = 100
	worker2 = spawn(
		WorkerX(a,a,a)
	)
	show('workers spawned')

	## wait for awhile before getting messages ##
	window.setTimeout(
		lambda: test_workers(worker1,worker2),
		1500,
	)


def test_workers(worker1, worker2):
	show('sending data to workers')
	msg = {
		'x':1, 
		'y':2,
		'z':3
	}

	for i in range(10):
		worker1 <- msg
		worker2 <- msg

	sleep(0.5)

	show('testing workers')

	results = []
	with timeout( 10 ):
		print 'in timeout'
		while True:
			select:
				case res = <- worker1:
					show('case-worker1:' + res)
					results.append( res )
				case res = <- worker2:
					show('case-worker2:' + res)
					results.append( res )

	print results


window.setTimeout(test, 1000)

```
