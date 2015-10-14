WebWorkers
-------

WebWorkers is a browser standard that allows you to use the extra CPU cores on the client.

https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers


html
----

@index.html
```html
<html>
<head>
</head>
<body onload="test()">
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
		def send(self,typedarr):
			avg = 0
			for i in range(typedarr.length):
				#print typedarr[i]
				avg += typedarr[i]
			return avg / typedarr.length

@debugger
def test():
	show('spawn workers')
	worker1 = spawn(
		Worker()
	)
	print 'worker1'
	print worker1
	## wait for awhile before sending messages ##
	window.setTimeout(
		lambda: test_workers(worker1),
		1500,
	)

def test_workers(worker1):
	show('sending data to worker')
	print worker1

	arr = [100]float32()  ## creates a fixed size Float32Array of size 100
	for i in range(100):
		arr[i] = i

	worker1 <- arr

	show('getting data from worker')
	res = <- worker1
	show('got first reply from worker')
	show(res)

	show('ok')

```
