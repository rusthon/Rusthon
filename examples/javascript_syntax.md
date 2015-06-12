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

def hello_world():
	window.alert("hi R arrow -> and L arrow <- and $ $. $(")

X = []

def test():
	global X
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

	X = [1,2]
	arr = [3,4]
	X += arr
	print X





window.setTimeout(test, 1000)

```
