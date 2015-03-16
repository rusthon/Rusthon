c staticlib
------
this C code gets compiled by gcc, compiled to its own staticlib, and linked into the main c++ program.
```c
#include <stdio.h>

void say_hi_c() {
	printf("Hello world from C\n");
}
```

c++
--------
```c++
#include <fstream>
#include <iostream>
#include <string>

void say_hi_cpp() {
	std::cout << std::string("hello world from c++") << std::endl;
}

```

rusthon
----------
```rusthon
#backend:c++

with extern():
	def say_hi_c(): pass

def say_hi():
	print( 'hello world')

def main():
	say_hi()
	say_hi_cpp()
	say_hi_c()
```


