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
TODO - fixme
-----
```
brett@mint15 ~/Rusthon $ ./rusthon.py ./examples/example-project.md
/tmp/cciqegbV.o: In function `say_hi_cpp()':
rusthon-build.cpp:(.text+0x0): multiple definition of `say_hi_cpp()'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0x0): first defined here
/tmp/cciqegbV.o: In function `str(std::string)':
rusthon-build.cpp:(.text+0x94): multiple definition of `str(std::string)'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0x94): first defined here
/tmp/cciqegbV.o: In function `str(int)':
rusthon-build.cpp:(.text+0xbd): multiple definition of `str(int)'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0xbd): first defined here
/tmp/cciqegbV.o: In function `__open__(std::string)':
rusthon-build.cpp:(.text+0xe3): multiple definition of `__open__(std::string)'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0xe3): first defined here
/tmp/cciqegbV.o: In function `range1(int)':
rusthon-build.cpp:(.text+0x161): multiple definition of `range1(int)'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0x161): first defined here
/tmp/cciqegbV.o: In function `range2(int, int)':
rusthon-build.cpp:(.text+0x202): multiple definition of `range2(int, int)'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0x202): first defined here
/tmp/cciqegbV.o: In function `ord(std::string)':
rusthon-build.cpp:(.text+0x2b9): multiple definition of `ord(std::string)'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0x2b9): first defined here
/tmp/cciqegbV.o: In function `__float__(std::string)':
rusthon-build.cpp:(.text+0x2df): multiple definition of `__float__(std::string)'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0x2df): first defined here
/tmp/cciqegbV.o: In function `round(double, int)':
rusthon-build.cpp:(.text+0x310): multiple definition of `round(double, int)'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0x310): first defined here
/tmp/cciqegbV.o: In function `say_hi()':
rusthon-build.cpp:(.text+0x364): multiple definition of `say_hi()'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0x364): first defined here
/tmp/cciqegbV.o: In function `main':
rusthon-build.cpp:(.text+0x3f8): multiple definition of `main'
/tmp/ccjzfNwN.o:rusthon-build.cpp:(.text+0x3f8): first defined here
collect2: error: ld returned 1 exit status
Traceback (most recent call last):
  File "./rusthon.py", line 420, in <module>
    package = build(modules, base_path )
  File "./rusthon.py", line 335, in build
    subprocess.check_call( cmd )
  File "/usr/lib/python2.7/subprocess.py", line 542, in check_call
    raise CalledProcessError(retcode, cmd)
subprocess.CalledProcessError: Command '['g++', '-static', '/tmp/rusthon-build.cpp', '-L/tmp/.', '-lrusthon-clib0', '/tmp/rusthon-build.cpp', '-o', '/tmp/rusthon-bin', '-pthread', '-std=c++11']' returned non-zero exit status 1

```

