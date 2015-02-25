Nim
--------------
TODO fix printing s, `echo(s)` segfaults
```nim
proc my_nim_function( s:cint ) {.cdecl, exportc.} =
	echo("calling my_nim_function")


```


Rusthon
---------------------------

```rusthon
#backend:c++

with extern(abi="C"):
	def my_nim_function( s:int ): pass


def main():
	print 'calling nim function'
	my_nim_function( 100 )
	print 'ok'

```