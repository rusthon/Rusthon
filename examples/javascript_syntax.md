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

chan = Channel()
with mymacro as "chan.send(JSON.stringify(%s))":
	mymacro( s3 )

def hello_world():
	window.alert("hi R arrow -> and L arrow <- and $ $. $(")


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

	for i,e in enumerate(X):
		print i, e




window.setTimeout(test, 1000)

```
