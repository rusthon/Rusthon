JavaScript Backend - Static Typed Dictionary
-------

https://github.com/rusthon/Rusthon/issues/70

To run this example, install nodejs, and run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_typed_dict.md
```


Example
--------

@myapp.js
```rusthon
#backend:javascript
from runtime import *

def foo( d:map[string]int ):
	print d
	print 'foo OK'

def bar( d:map[int]string ):
	print d
	print 'bar OK'

@debugger
def test():
	a = map[string]int{}
	a['x'] = 1
	a['y'] = 2

	b = map[int]string{
		10 : 'w',
		11 : 'z'
	}

	foo( a )
	bar( b )

	## below is not allowed by the type system
	## uncomment these to see them throw TypeError
	#foo( b )
	#bar( a )

test()

```

HTML
--------

@index.html
```html
<html>
<head>
</head>
<body>
<@myapp.js>
</body>
</html>
```