c++
--------
```c++
#include <fstream>
#include <iostream>
#include <string>
void say_hi_cpp() {
	std::cout << std::string("hello world from c++") << std::endl;
}

extern "C" {
	void say_hi_c();
}

```

rusthon
----------
```rusthon

def say_hi():
	print( 'hello world')

def main():
	say_hi()
	say_hi_cpp()
	say_hi_c()
```


c staticlib
------
this C code gets compiled by gcc and linked into the main program
```c
#include <stdio.h>
void say_hi_c() {
	printf("Hello world from C\n");
}
```
