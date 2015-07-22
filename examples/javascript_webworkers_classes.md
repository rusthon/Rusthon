

@myapp
```rusthon
#backend:javascript
from runtime import *

def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)

class SharedClass:
	def __init__(self, x,y,z):
		self.x = x
		self.y = y
		self.z = z

	def foobar(self):
		return self.x + self.y + self.z


with webworker:
	class MyWorker:
		def send(self, obj:SharedClass ):
			print obj
			print obj.foobar()
			obj.x = 10
			return obj


def main():
	global WORKER
	show('spawn worker...')
	WORKER = spawn( MyWorker() )
	show('creating SharedClass')
	a = SharedClass(1,2,3)
	print(a)
	show(a.foobar())
	show('sending data to worker')
	WORKER <- a
	show('getting data from worker')
	b = <- WORKER
	print(b)
	#print b.foobar()


```

@index.html
```html
<html>
<head>
</head>
<body onload="main()">
<pre id="CONTAINER">
</pre>
<@myapp>
</body>
</html>
```