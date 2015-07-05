testing
-------

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_timeout_loops.md
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


@myscript
```rusthon
#backend:javascript
from runtime import *

def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)


def CalcFib(n):
	if n == 0: return 0
	elif n == 1: return 1
	else: return CalcFib(n-1)+CalcFib(n-2)


def test():
	show('start async test')
	que = []

	show( 'LOOP1 - 10ms' )
	with timeout( 10 ):
		show( 'calc fib 16-32' )
		for i in range(16, 32):
			que.append( CalcFib(i) )

		show( 'calc fib 8-16' )

		for i in range(8,16):
			que.append( CalcFib(i) )

		show( 'calc fib 8' )

		for i in range(8):
			que.append( CalcFib(i) )


	show( len(que) )
	print que

	show( 'LOOP2 - 10ms' )
	show( 'calc fib 32' )
	q = []
	with timeout( 10 ):
		for i in range(32):
			q.append( CalcFib(i) )

	show( len(q) )
	print q

	show( 'WHILE LOOP - 10ms' )
	show( 'calc fib 32' )
	q = []
	with timeout( 10 ):
		i = 0
		while True:
			q.append( CalcFib(i) )
			i += 1

	show( len(q) )
	print q

	show('end async test')


window.setTimeout(test, 1000)

```
