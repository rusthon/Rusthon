testing
-------

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/hello_javascript.md
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

Above a special syntax is used `@myscript` this tells Rusthon where to insert the output of scripts it translates using the javascript backend below.


rusthon javascript backend
--------------------------

Below `@myscript` is given on the line just before the fenced rusthon code block.  This allows you to insert multiple scripts into your html, in the head or body.

@myscript
```rusthon
#backend:javascript
from runtime import *

def hello_world():
	window.alert("hi")

```
