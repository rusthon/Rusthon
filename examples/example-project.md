Rusthon Markdown Compiler
=========================
rusthon.py can be given a markdown file `.md` and code blocks will be extracted and compiled.
This is inspired by CoffeeScript literate format, http://coffeescript.org/#literate

Fenced code blocks with the syntax highlight tag are used to translate and build the project,
the supported languages are: `rusthon`, `c++`, `rust`, `javascript`, `python`
Code blocks tagged as `javascript` or `python` are saved to the output tar file.
Fenced code blocks without a syntax highlight tag are ignored.

```
cd Rusthon
./rusthon.py ./examples/example-project.md --tar
```
Above if `--tar` is not given then the result is run after being compiled by `rustc` and `g++`.

some c++
--------
the function below `say_hi_cpp` can be directly called from the rusthon code below,
because the default backend for rusthon is c++.

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
The code below is translated to C++ and merged with the hand written C++ code above.

```rusthon
def say_hi():
	print( 'hello world')

def main():
	say_hi()
	say_hi_cpp()
```

cpython script
-------------
```python
print('cpython script')
```

javascript
-------
```javascript
window.alert('hi');
```

go
-------
This hand written Go code is callable from the rusthon code below.
```go
func my_go_func() {
	fmt.Println("hello world from Go.")
}
func call_rusthon_func_from_go() {
	my_rusthon_func()
}
```

rusthon go backend
------------------
The backend is selected by the special comment on the first line of the script,
below the Go backend is set by `#backend:go`.
When using the Go backend, hand written Go code can be called directly,
the call below `my_go_func` is defined above.
```rusthon
#backend:go

def my_rusthon_func():
	print('my rusthon func called from go')

def main():
	print('hello from rusthon go backend')
	my_go_func()
	call_rusthon_func_from_go()
```

