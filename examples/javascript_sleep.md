Sleep - Async
-------------

async javascript functions made easy.


To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_sleep.md
```

html
----


@index.html
```html
<html>
<head>
<@myscript>
</head>
<body onload="test()">
<pre id="CONTAINER">
</pre>
</body>
</html>
```

Example
--------------------------

`sleep(seconds)` pauses a function for a given number of seconds,
it can only be used in the function body, and not under any conditional blocks or loops.

@myscript
```rusthon
#backend:javascript
from runtime import *

def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)

def invalid_sleep():
	## sleep is not allowed under any control or loop blocks
	## uncomment below to see a transpiler error
	#if True:
	#	show('sleep2')
	#	sleep(1)
	#else:
	#	show('never seen')
	#for i in range(10):
	#	sleep(1)
	#while True:
	#	sleep(1)
	#	break
	pass

@debugger
def test():

	show('sleep1')

	sleep(1)

	show('sleep2')
	sleep(1)

	show('sleep3')
	sleep(1)

	show('sleep test OK')


```
