Testing
-------
This gets compiled and run with:
```bash
./rusthon.py ./examples/hello_nim.md
```
Note you need to have Nim installed in your home directory so Rusthon can find it.

Nim
--------------
Below is a simple function in Nim.  The Nim compiler is used to transform this to C.  
The Nim runtime and generated code is then merged into a single C file and built as a static library by Rusthon.  
This static library is then linked to the final C++ exe below.

The Nim program below is parsed by Rusthon, any functions that export to C using the pragma `{.cdecl, exportc.}`
will wrappers generated for them so they can be called when linked to the final C++ exe.
The wrapper functions are declared as `extern "C"`.


```nim
proc my_nim_function( a:cint, b:cint ): cint {.cdecl, exportc.} =
	echo("calling my_nim_function")
	echo("a:", a)
	echo("b:", b)
	result = a+b

```


Rusthon
---------------------------
Nim functions that you want to expose to Rusthon need to be declared inside a `with extern(abi="C"):` block.
note: `nim` must be imported and `nim.main` must be called before calling any nim functions.


```rusthon
#backend:c++
import nim

def main():
	nim.main()
	print 'calling nim function'
	msg = my_nim_function( 10, 20 )
	print msg
	print 'ok'

```




TODO
-----
* fix return `cstring` when trying to call `GC_ref(result)` nim throws this error: 
```
Error: type mismatch: got (cstring)
but expected one of: 
system.GC_ref(x: seq[T])
system.GC_ref(x: string)
system.GC_ref(x: ref T)
```
