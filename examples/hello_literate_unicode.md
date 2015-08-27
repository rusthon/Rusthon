command line: `--literate-unicode`

https://github.com/rusthon/Rusthon/wiki/JavaScript-Unicode-Literate-Output


html
----

@index.html
```html
<html>
<head>
<script src="~/ace-builds/src-min/ace.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/theme-monokai.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/worker-javascript.js" type="text/javascript"></script>
<script src="~/ace-builds/src-min/mode-javascript.js" type="text/javascript"></script>
<@js>
<@py>
</head>
<body onload="test()">
</body>
</html>
```

javascript
----------

https://mothereff.in/js-variables

@js
```javascript

function 𝓩add( x,y ) {
	return {𝓩:x+y}
};

var 𝑭𝑶𝑶𝒃𝒂𝒓 = {
	𝓨 : function (x,y) {
		𝑷𝒓𝒊𝒏𝒕(x+y); 
		return 𝓩add(x,y);
	},
	x : 20
};

var 𝒃𝒂𝒓 = 'UNICODE_OK';
var 𝓦 = {
		𝓧  : 𝑭𝑶𝑶𝒃𝒂𝒓,
		𝒃𝒂𝒓 : 'xxx'
};

var W = 𝓦;

```

Transpiled
----------

@py
```rusthon
#backend:javascript
from runtime import *

def 𝕬( a ):
	return a * 2


class ꘐ:
	def __init__(self):
		self.name = '៘'

class 𝔇𝕆𝔊( ꘐ ):

	def bark(self, say):
		print say
		alert(self.name)

@debugger
def test():
	foobar = 𝑭𝑶𝑶𝒃𝒂𝒓
	assert 𝒃𝒂𝒓 == 'UNICODE_OK'
	print foobar

	print 𝓦.𝓧.𝓨(foobar).𝓩
	𝓦.𝓧.𝒃𝒂𝒓 = 'bar'

	assert 𝕬( 2 ) == 4


	with ꘚ as "console.log(%s)":
		ꘚ( 'macro ok')

	with ꗈ as "document.body.appendChild(%s)":
		with ꗢ as "document.createElement(%s)":
			with 𝕋𝕏𝕋 as "e.appendChild(document.createTextNode(%s))":
				for i in range(10):

					e = ꗢ('div')
					ꗈ( e )
					𝕋𝕏𝕋('macro:'+i)

					e = ꗢ('button')
					ꗈ( e )
					𝕋𝕏𝕋('mybutton:'+i)


	#a.x.y = 'oopps'
	#show( some_missing_object[ 'x' ] )
	#mytypo()

	dog = 𝔇𝕆𝔊()
	dog.bark('woof')


```
