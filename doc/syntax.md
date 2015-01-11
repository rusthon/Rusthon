Classes
=========
https://github.com/rusthon/Rusthon/blob/master/regtests/rust/simple_subclass.py
https://github.com/rusthon/Rusthon/blob/master/regtests/rust/multiple_inheritance.py


Go Style Syntax
===============
  . works with backends: go, rust, c++

typed arrays
---------
```go
a = []int(1,2,3)
b = []int(x for x in range(3))
push_something( a )
```
function array typed parameters
------------------------------
the `append` method is translated to work with each backend.
```python
def push_something( arr:[]int ):
	arr.append( 4 )
```
https://github.com/rusthon/Rusthon/blob/master/regtests/rust/list_comp.py

typed maps
---------
```go
a = map[string]int{'a':1, 'b':2}

```
map iteration
-------------
The key value pairs can be looped over with a for loop.
```python
	def main():
		a = map[string]int{'x':100, 'y':200}
		b = ''
		c = 0
		for key,value in a:
			b += key
			c += value
```


async channels
--------------
https://github.com/rusthon/Rusthon/blob/master/regtests/rust/chan_universal_style.py
```python
sender, recver = channel(int)
```

<- send data
---------
```go
a <- b
```

channel select
--------------
switches to a given case when the channel data is ready.
```go
select:
	case x = <- a:
		y += x
	case x = <- b:
		y += x
```

function channel parameter types
--------------------------------
```python
def sender_wrapper( sender: chan Sender<int> ):
	sender <- 100

def recv_wrapper(recver: chan Receiver<int> ):
	result = <- recver
```

Javascript Style Syntax
=======================

switch
-------
```javascript
switch a == b:
	case True:
		x = z
	case False:
		y = z
	default:
		break

```

var
----
. `var ` is allowed before a variable name in an assignment.
```javascript
	var x = 1
```

new
----
. 'new' can be used to create a new JavaScript object
```python
	a = new SomeObject()
```

$
----
. `$` can be used to call a function like jquery
```python
	$(selector).something( {'param1':1, 'param2':2} )
```

. External Javascript functions that use an object as the last argument for optional named arguments, can be called with Python style keyword names instead.
```python
	$(selector).something( param1=1, param2=2 )
```

. `$` can be used as a funtion parameter, and attributes can be get/set on `$`.
```python
def setup_my_jquery_class( $ ):
	$.fn.someclass = myclass_init
```

. function expressions
```python
F = def(x):
	return x
```


exception expressions
-------------------------------
this is a shortcut for writting simple try/except blocks that assign a value to a variable
(PEP 463)
```python
a = {}
b = a['somekey'] except KeyError: 'my-default'
```


Invalid Syntax
=======================
  . `with` is reserved for special purposes.  
  . `for/else` and `while/else` are deprecated.