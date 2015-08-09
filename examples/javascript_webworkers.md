WebWorkers
-------

WebWorkers is a browser standard that allows you to use the extra CPU cores on the client.

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_webworkers.md
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
	class Worker():
		def send(self,ob):
			## do some long computation here ##
			return ob

@debugger
def test():
	show('spawn workers')
	worker1 = spawn(
		Worker()
	)
	worker2 = spawn(
		Worker()
	)
	## wait for awhile before sending messages ##
	window.setTimeout(
		lambda: test_workers(worker1,worker2),
		1500,
	)

def test_workers(worker1, worker2):
	show('sending data to workers')
	worker1 <- 'msg 1'
	worker1 <- 'msg 2'
	worker1 <- 'msg 3'
	worker1 <- 'msg 4'

	worker2 <- 'msg 5'
	worker2 <- 'msg 6'
	worker2 <- 'msg 7'
	worker2 <- 'msg 8'

	show('getting data from workers')
	res = <- worker1
	show('got first reply from worker')
	show(res)
	res = <- worker1
	show(res)
	res = <- worker1
	show(res)
	res = <- worker1
	show(res)

	res = <- worker2
	show(res)
	res = <- worker2
	show(res)
	res = <- worker2
	show(res)
	res = <- worker2
	show(res)

	show('ok')



window.setTimeout(test, 1000)

```
