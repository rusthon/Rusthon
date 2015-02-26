Nim
--------------

```nim
proc my_nim_function( s:cint ) {.cdecl, exportc.} =
	echo("calling my_nim_function")
	echo(s)
```


Rusthon
---------------------------
note: NimMain must be called to setup GC.

```rusthon
#backend:c++

with extern(abi="C"):
	def my_nim_function( s:int ): pass
	def NimMain(): pass


def main():
	NimMain()
	print 'calling nim function'
	my_nim_function( 100 )
	print 'ok'

```