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

TODO fix syntax highlighting on github:
https://github.com/github/linguist/pull/2001
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
```go
package main
import "fmt"
func main() {
	fmt.Println("hello world")
}
```



