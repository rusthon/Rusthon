Nim
--------------
TODO fix printing s, `echo(s)` segfaults
```nim
proc my_nim_function( s:cint ) {.cdecl, exportc.} =
	echo("calling my_nim_function")


```

c++ wrapper
```c++
extern "C" {
	void my_nim_function(int s);
}

```

Rusthon
---------------------------

```rusthon
#backend:c++

def main():
	print 'calling nim function'
	my_nim_function( 100 )
	print 'ok'

```