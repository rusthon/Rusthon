JavaScript Backend - Gotchas
-------

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Object_initializer#Computed_property_names

@myapp.js
```rusthon
#backend:javascript
from runtime import *

def foo():
	return 'FOO'

def test():
	print 'testing javascript gotchas'
	a = 'bar'
	d = {
		a : 2,
		foo() : 1
	}
	print d

	## dict literals follow javascript initalization rules,
	## where `a` is treated as an unquoted string literal,
	## instead of the variable  
	assert d[ a ] is undefined
	assert d[ 'a' ] == 2

	## this works because the transpiler is able to infer
	## in the construction of `d` that `foo()` is a function
	## call and not an unquoted string literal.
	assert d[foo()] == 1

	## part of the new javascript standard ES6, allows for `Computed Property Names`,
	## by wrapping your key in `[]` the key value becomes an expression, and not an unquoted string literal.
	## Rusthon also supports this syntax, and transpiles it to javascript that will run in pre-ES6 browsers.
	d = {
		[a] : 1
	}
	assert d[a] == 1
	print d

	print 'test ok'

test()

```

