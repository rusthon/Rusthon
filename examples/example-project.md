Rusthon Markdown Compiler
=========================
rusthon.py can be given a markdown file `.md` and code blocks will be extracted and compiled.
This is inspired by CoffeeScript literate format, http://coffeescript.org/#literate

Fenced code blocks with the syntax highlight tag are used to translate and build the project,
the supported languages are: `rusthon`, `c++`, `rust`, 'javascript', 'python'
Code blocks tagged as `javascript` or `python` are saved to the output tar file.
Fenced code blocks without a syntax highlight tag are ignored.

```
cd Rusthon
./rusthon.py ./examples/example-project.md --tar
```
Above if `--tar` is not given then the result is run after being compiled by `rustc` and `g++`.

some c++
--------
```c++
#include <fstream>
#include <iostream>
#include <string>
void say_hi_cpp() {
	std::cout << std::string("hello world from c++") << std::endl;
}

```

helloworld
----------
```rusthon

def say_hi():
	print( 'hello world')

def main():
	say_hi()
	say_hi_cpp()

```

python script
-------------
```python
print('cpython script')
```