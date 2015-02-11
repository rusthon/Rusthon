Nim
--------------

```nim
proc my_nim_function( s:cint ) {.exportc: "callNimFunc", varargs.} =
	echo("calling my_nim_function")
	echo( s )

```

c++ wrapper
```
extern "C" {
	void callNimFunc(int s);
}

```

Rusthon
---------------------------

```rusthon
#backend:c++

def main():
	callNimFunc( 100 )

```