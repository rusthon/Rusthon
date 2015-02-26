Nim
--------------
Below is a simple function in Nim.  The Nim compiler is used to transform this to C.  The Nim runtime and generated code is then merged into a single C file and built as a static library by Rusthon.  This static library is then linked to the final C++ exe below.
```nim
proc my_nim_function( s:cint ) {.cdecl, exportc.} =
	echo("calling my_nim_function")
	echo(s)
```


Rusthon
---------------------------
Nim functions that you want to expose to Rusthon need to be declared inside a `with extern(abi="C"):` block.
note: `nim` must be imported and `nim.main` must be called before calling any nim functions.

```rusthon
#backend:c++
import nim

with extern(abi="C"):
	def my_nim_function( s:int ): pass


def main():
	nim.main()
	print 'calling nim function'
	my_nim_function( 100 )
	print 'ok'

```