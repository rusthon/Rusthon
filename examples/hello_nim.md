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
will have wrappers generated for them so they can be called when linked to the final C++ exe.
The wrapper functions are declared as `extern "C"`.


```nim
proc my_nim_function( a:cint, b:cint, s:cstring ): cint {.cdecl, exportc.} =
	echo("calling my_nim_function")
	echo(s)
	echo("a:", a)
	echo("b:", b)
	result = a+b

```


Rusthon
---------------------------
note: `nim` must be imported and `nim.main` must be called before calling any nim functions.
note: below in the call to `my_nim_function` the string `s` is wrapped to `cstr` to convert it to a C string type `const char*`

```rusthon
#backend:c++
import nim

def main():
	nim.main()
	print 'calling nim function'
	s = 'mymessage to nim'
	msg = my_nim_function( 10, 20, cstr(s) )
	print msg
	print 'ok'

```




TODO
-----
* return a cstring and convert it to a std::string
* fix return `cstring` when trying to call `GC_ref(result)` nim throws this error: 
```
Error: type mismatch: got (cstring)
but expected one of: 
system.GC_ref(x: seq[T])
system.GC_ref(x: string)
system.GC_ref(x: ref T)
```
