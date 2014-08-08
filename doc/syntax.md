PythonJS Syntax
===============

PythonJS extends the Python language with new keywords, syntax,
and optional static typing.


switch
-------
```
switch a == b:
	case True:
		x = z
	case False:
		y = z
	default:
		break

```

exception expressions (PEP 463)
-------------------------------
this is a shortcut for writting simple try/except blocks that assign a value to a variable
```
a = {}
b = a['somekey'] except KeyError: 'my-default'
```

inline def
----------
in a function call, inline functions can be given as keyword arguments.
```
a.func(
	callback1=def (x,y,z):
		x += y
		return x - z,
	callback2= def (x, y):
		return x * y
)
```

inline functions can also be used inside a dict literal
```
a = {
	'cb1' : def (x):
		return x,
	'cb2' : def (y):
		return y
}
```

<- send data
---------
note: only works with Go backend
```
a <- b
```

typed arrays and maps
---------
note: only works with Go backend
```
a = []int(1,2,3)
b = map[string]int{'a':1, 'b':2}
```

channel select
--------------
switches to a given case when the channel data is ready.
note: only works with Go backend
```
select:
	case x = <- a:
		y += x
	case x = <- b:
		y += x
```

var
----
. it is ok to have `var ` before a variable name in an assignment.
```
	var x = 1
```

new
----
. 'new' can be used to create a new JavaScript object
```
	a = new SomeObject()
```

$
----
. `$` can be used to call a function like jquery
```
	$(selector).something( {'param1':1, 'param2':2} )
```

. External Javascript functions that use an object as the last argument for optional named arguments, can be called with Python style keyword names instead.
```
	$(selector).something( param1=1, param2=2 )
```

. `$` can be used as a funtion parameter, and attributes can be get/set on `$`.
```
def setup_my_jquery_class( $ ):
	$.fn.someclass = myclass_init
```

->
-----
. `->` can be used to as a special attribute operator for passing methods that will automatically bind
the method's `this` calling context.  This enables you to pass methods as callbacks to other objects,
and not have to write `a.some_method.bind(a)`
```
	b.set_callback( a->some_method )
```


function expressions
--------------------
```
F = function(x):
	return x
```


Invalid PythonJS Syntax
=======================
PythonJS deprecates two types of syntax from the Python language.  The use of the `with` statement is reserved for special purposes.  And the syntax `for/else` and `while/else` are deprecated.