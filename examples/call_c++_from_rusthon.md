TODO: fix subclass and constructors.

```c++
#include <fstream>
#include <iostream>
#include <string>

class HelloWorld {
  public:
	std::string mystring;
	void mymethod();
	void set( std::string s ) { this->mystring = s;}
};
	void HelloWorld::mymethod() {
		std::cout << this->mystring << std::endl;
	}

void bar( HelloWorld* ob ) {
	ob->mymethod();
}

```

`Subclass` defines `__init__` to workaround the problem of calling the parent constructor
of an external c++ class.

```rusthon
#backend:c++

class Subclass( HelloWorld ):
	def __init__(self, s:string ):
		self.set( s )

	def foo(self):
		print 'foo'

def main():
	ob = new(HelloWorld())
	ob.set('hi')
	ob.mymethod()
	print ob
	bar( ob )

	s = new(Subclass('hey'))
	print s
	s.mymethod()
	s.foo()


```