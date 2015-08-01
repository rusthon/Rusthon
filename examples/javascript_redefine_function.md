
@myapp
```rusthon
#backend:javascript
from runtime import *

def show(txt):
	document.getElementById('CONTAINER').appendChild(
		document.createTextNode(txt + '\n')
	)

def bar():
	show('bar original')
	show(bar.redef)
	if bar.redef is not undefined:
		if bar.newcode is not undefined:
			eval('bar.redef='+bar.newcode)
			bar.newcode = undefined
		return bar.redef.apply(None, arguments)

	def F(x,y):
		show('bar changed')
		show( x+y )

	bar.redef = F
	show('only shows once')

def redefine_bar():
	code = document.getElementById('CODE').value
	print code
	bar.newcode = code

def main():
	bar()
	bar(1,1)
	bar(2,2)
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
<input type="text" id="CODE" value="function f(){show('hello world')}"/>
<input type="button" onclick="redefine_bar();bar()"/>
</body>
</html>
```