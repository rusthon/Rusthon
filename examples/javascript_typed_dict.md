JavaScript Backend - Static Typed Dictionary
-------

Runtime checked typed hashmaps are implemented by attaching a two special hidden methods to
each typed hashmap: `__setitem__` and `__getitem__`.

Note class instances can be used as dict keys,
this is done by inserting a special `toString` method into each class prototype,
and in the constructor incrementing a hidden `uid` that `toString` returns.

More info:
https://github.com/rusthon/Rusthon/wiki/JavaScript-Static-Types

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

class MyClass:
	def __init__(self,x:int, y:int):
		self.x = x
		self.y = y


@debugger
def test():
	global a, b, c

	a = map[string]int{}
	a['x'] = 1
	a['y'] = 2

	b = map[int]string{
		10 : 'w',
		11 : 'z',
		#'bad' : 'x'
	}
	## these calls are ok ##
	foo( a )
	bar( b )

	## below is not allowed by the type system
	## uncomment these to see them throw TypeError
	#a[ 0 ]   = 1     ## this is an invalid keytype
	#a[ 'z' ] = 'bad' ## invalid value type
	#foo( b )
	#bar( a )

	v1 = MyClass(1,2)
	v2 = MyClass(3,4)
	v3 = MyClass(4,5)
	c = map[MyClass]int{
		v1 : 10,
		v2 : 20,
		#'bad' : 30
	}
	assert c[v1] == 10
	assert c[v2] == 20

	c[ v1 ] = 100
	c[ v2 ] = 200

	assert v1 in c
	assert v2 in c
	assert v3 not in c

	assert c[v1] == 100
	assert c[v2] == 200

	## this fails
	#c[ 'badkey' ] = 1

	print 'typed hashmaps OK'

test()

```

