JavaScript Backend - Static Types
-------

Enables runtime static type checking.

To run this example run these commands in your shell:

```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon/
./rusthon.py ./examples/javascript_static_types.md
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
see the javascript console for test results
</body>
</html>
```

Example
--------

notes:
* the `float` type is true for any number, because `0.0` becomes `0`

@myscript
```rusthon
#backend:javascript
from runtime import *

class A:
	def foo( self, x:B ):
		print 'foo'
		print x

	def test_int( self, x:int ):
		print x

	def test_float( self, x:float ):
		print x

class B:
	def bar( self, x:A ):
		print 'bar'
		print x


def test():
	a = A()
	b = B()
	a.foo( b )
	#a.foo( 1 )  ## not allowed, throw error
	b.bar( a )

	a.test_int( 1 )
	a.test_float( 1.1 )

test()

```