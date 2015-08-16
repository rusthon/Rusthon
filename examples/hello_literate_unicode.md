testing
-------

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/hello_rapydscript.md
```

html
----


@index.html
```html
<html>
<head>
<@js>
<@py>
</head>
<body onload="test()">
</body>
</html>
```

@js
```javascript

var 𝑭𝑶𝑶𝒃𝒂𝒓 = 'UNICODE_OK';

```


@py
```rusthon
#backend:javascript
from runtime import *

@debugger
def test():
	foobar = inline('𝑭𝑶𝑶𝒃𝒂𝒓')
	assert foobar == 'UNICODE_OK'
	print foobar

```
