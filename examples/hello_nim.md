Nim
--------------

```nim
proc my_nim_function( s:cint ) {.cdecl, exportc.} =
	echo("calling my_nim_function")
	echo( s )


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
	my_nim_function( 100 )

```