Testing
-------
This gets compiled and run with:
```bash
./rusthon.py ./examples/hello_nim.md
```
Note you need to have Nim installed in your home directory so Rusthon can find it.

Nim
--------------
Below is a simple function in Nim.  The Nim compiler is used to transform this to C.  The Nim runtime and generated code is then merged into a single C file and built as a static library by Rusthon.  This static library is then linked to the final C++ exe below.
```nim
proc my_nim_function( s:cint ): cstring {.cdecl, exportc.} =
	echo("calling my_nim_function")
	echo(s)
	var v = "hi"
	result = v

```


Rusthon
---------------------------
Nim functions that you want to expose to Rusthon need to be declared inside a `with extern(abi="C"):` block.
note: `nim` must be imported and `nim.main` must be called before calling any nim functions.

```rusthon
#backend:c++
import nim

with extern(abi="C"):
	def my_nim_function( s:int ) -> cstring:
		pass


def main():
	nim.main()
	print 'calling nim function'
	msg = my_nim_function( 100 )
	print msg
	print 'ok'

```