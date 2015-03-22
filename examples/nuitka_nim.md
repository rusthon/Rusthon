
Nim
--------------

```nim
proc my_nim_function( a:cint, b:cint, s:cstring ): cint {.cdecl, exportc.} =
	echo("calling my_nim_function")
	echo(s)
	echo("a:", a)
	echo("b:", b)
	result = a+b

```

Nuitka Class
------------
Class `A`

@nuitka:mymodule
```python

class A():
	def pymethod(self, msg):
		print 'hello world from nuitka:', msg

```


Build Options
-------------
* @link:python2.7
* @include:/usr/include/python2.7

```rusthon
#backend:c++
import nim
import cpython

def main():
	ts = cpython.initalize()
	nim.main()
	print 'calling nim function'
	s = 'mymessage to nim'
	msg = my_nim_function( 10, 20, cstr(s) )
	print msg
	with gil:
		a = cpython.A()
		a->pymethod( msg as pyint )
	print 'OK'
	cpython.finalize(ts)
```
