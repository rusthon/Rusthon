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
<script src="~/ace-builds/src-min/ace.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/theme-monokai.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/worker-javascript.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/mode-javascript.js" type="text/javascript"></script>


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

function 𝓩add( x,y ) {
	return {𝓩:x+y}
}


var 𝑭𝑶𝑶 = {
	𝓨 : function (x,y) {console.log(x+y); return 𝓩add(x,y)},
	x : 20
}
var 𝒃𝒂𝒓 = 'UNICODE_OK';
var 𝓦 = {
		𝓧  : 𝑭𝑶𝑶,
		𝒃𝒂𝒓 :


```


@py
```rusthon
#backend:javascript
from runtime import *

𝕬 = 1

@debugger
def test():
	foobar = 𝑭𝑶𝑶𝒃𝒂𝒓
	assert foobar == 'UNICODE_OK'
	print foobar

	print 𝓦.𝓧.𝓨(foobar).𝓩
	𝓦.𝓧.𝒃𝒂𝒓 = 'bar'

	a.x.y = 'oopps'
	#x( 𝓓𝓔𝓕 )
	show( some_missing_object[ 'x' ] )
	mytypo()

```
