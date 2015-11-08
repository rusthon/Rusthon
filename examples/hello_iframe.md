iframe html
----

@myiframe.html
```html
<html>
<head>
</head>
<body>
<h1 id="FOO">Hello Iframe</h1>
</body>
</html>
```

main html
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

Script
---------------

@myscript
```rusthon
#backend:javascript
from runtime import *

@debugger
def hello_world():
	iframe = document->('iframe')->(src='myiframe.html')
	document.body->(iframe)
	global doc
	sleep(1)
	doc = iframe.contentDocument
	h1  = doc->('#FOO')
	print h1
	sleep(1)
	h1->('foo')
	h1->( doc->('a')->('bar', href="http://...") )


```
