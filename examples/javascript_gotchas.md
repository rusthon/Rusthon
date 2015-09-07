JavaScript Backend - Gotchas
-------


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

	print 'test ok'

test()

```

