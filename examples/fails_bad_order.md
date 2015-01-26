C++ Gotcha
----------
If your comming from Python, nothing looks wrong with the program below.  Your thinking of course g++ is going to do a second pass and find the definition of `otherfunc` and use it in `main` - sadly this is **not** how it works in C/C++.

```rusthon
#backend:c++

def main():
	otherfunc()

def otherfunc():
	print('hi')
```

Rusthon makes no attempt to reorder your functions so that they can be compiled by g++.  So for now you need to pay attention to how you order functions that depend on one another.  In the future this will be fixed with forward declarations of all functions in the header.  Until then, if you make this mistake, your going to see an error like this:
```
brett@mint15 ~/Rusthon $ ./rusthon.py ./examples/fails_bad_order.md
/tmp/rusthon-c++-build.cpp: In function ‘int main()’:
/tmp/rusthon-c++-build.cpp:64:12: error: ‘otherfunc’ was not declared in this scope
```
