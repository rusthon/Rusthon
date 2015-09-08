[![Build Status](https://travis-ci.org/rusthon/Rusthon.svg)](https://travis-ci.org/rusthon/Rusthon)

Easily mix multiple languages, frontends, backends, compilers, and transpilers inside markdown files.
Markdown is the container format for your multi-language application that can contain: server backend logic and config files,
and frontend javascript with html and css, all in a single markdown file.
Rusthon compiles the markdown into tar files for release, or runs it for testing.

The integrated Python transpiler targets multiple backend languages, like: JavaScript and C++.
The JavaScript backend implements most of the dynamic and some builtin functions of Python.
The C++ backend is less dynamic and uses an extended static type syntax based on Go, Rust and C++.
The other backends are experimental.

* [highlevel overview](http://rusthon-lang.blogspot.com/2015/06/rusthon-overview.html)
* [multiple markdown syntax](https://github.com/rusthon/Rusthon/wiki/Multiple-Markdowns)
* [professional training and support](http://rusthon-lang.blogspot.com/p/contract-me.html)

Installing
----------

* [Debian Package](https://github.com/rusthon/Rusthon/releases/download/0.9.9l/rusthon_0.9.0_all.deb)
* Fedora package comming soon

If you want to stay in sync with the git-repo, use the `install-dev.sh` script instead of the Debian or Fedora package. note: `install-dev.sh` just creates a symbolic link `transpile` that points to the current location of `rusthon.py`.


```bash
cd
git clone https://github.com/rusthon/Rusthon.git
cd Rusthon
sudo ./install-dev.sh
```


Using `transpile`
-----------------
To see all the command line options run `transpile --help`

```bash
cd myproject
transpile mymarkdown.md
```

Above will compile everything in mymarkdown.md:
* if the markdown contains an html page, it will be opened with NW.js or your system default web browser.
* if the markdown contains a javascript file, it will be run with nodejs
* otherwise, if the markdown contains: C++, Rust, or Go code, it will be compiled, and the exe is run.


Getting Started Javascript
-----------------
Transpile from Python to Javascript, with specialized syntax for static types, and using [WebWorkers](https://github.com/rusthon/Rusthon/wiki/WebWorker-Syntax) and other extensions to the Python language like [mini-macros](https://github.com/rusthon/Rusthon/wiki/Macro-Functions)

Mini-macros help you make your code more readable, and hide ugly API's like DOM.
note: you can use unicode for macro names.
```python
with 𝕄 as "_=document.createElement(%s); _.setAttribute('id',%s); %s.appendChild(_)":
    𝕄( 'div', 'someid1', document.body )
    𝕄( 'img', 'someid2', document.body )

```
* [javascript example](https://github.com/rusthon/Rusthon/blob/master/examples/javascript_syntax.md)
* [javascript backend wiki](https://github.com/rusthon/Rusthon/wiki/JavaScript-Backend)
* [javascript backend doc](https://github.com/rusthon/Rusthon/blob/master/doc/pythonjs.md)
* [javascript literate unicode](https://github.com/rusthon/Rusthon/wiki/JavaScript-Unicode-Literate-Output)


Extra JavaScript Frontends
--------------------
CoffeeScript and Rapydscript are great languages to use to avoid the pains of writing JavaScript by hand.
They can be directly included in the markdown files, and will get compiled to javascript.

To use these frontends install them on your system, they will be used as subprocesses
to output the final javascript.
* [coffee script](https://github.com/rusthon/Rusthon/blob/master/examples/hello_coffee.md)
* [rapydscript](https://github.com/rusthon/Rusthon/blob/master/examples/hello_rapydscript.md)


C++/Rust/Go Backends
--------------------

The C++11 backend is the most mature of the native compiled backends.
All the backends are regression tested, and the tests results are here:

* [c++ regression test results](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-c%2B%2B.md)
* [go regression test results](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-go.md)
* [rust regression test results](https://github.com/rusthon/Rusthon/blob/master/regtests/regtest-report-rust.md)


C++ Backend Docs
-----------
note: this and other backends are still a work in progress.

* [typed backend extra syntax](https://github.com/rusthon/Rusthon/blob/master/doc/syntax.md)
* [vectors](https://github.com/rusthon/Rusthon/wiki/Lists-and-Arrays)
* [concurrency](https://github.com/rusthon/Rusthon/wiki/concurrency)
* [cpython integration](https://github.com/rusthon/Rusthon/wiki/CPython-Integration)
* [arrays and generics](https://github.com/rusthon/Rusthon/wiki/Array-Generics)
* [java frontend](https://github.com/rusthon/Rusthon/wiki/Java-Frontend)
* [memory and reference counting](https://github.com/rusthon/Rusthon/blob/master/doc/memory.md)
* [weak references](https://github.com/rusthon/Rusthon/wiki/Weak-References)
* [nim integration](https://github.com/rusthon/Rusthon/wiki/Nim-Integration)

Getting Started - C++ Backend
-----------

![highleveloverview](http://rusthon.github.io/Rusthon/images/RusthonC++.svg)


After git cloning this repo, try async_channels.md, you just need Python2 and g++ installed.  The command below will save the compiled exe to your temp folder and run it.

```bash
cd Rusthon
./rusthon.py ./examples/async_channels.md
```
see [async_channels.md](https://github.com/rusthon/Rusthon/blob/master/examples/async_channels.md)

The option `--tar` can be used to save the source code of the translated code,
javascripts and python scripts inside the markdown, and compiled exes.
```
./rusthon.py myproject.md --tar project.tar
```


C++ and Rust - Classes and Callbacks
=====================================

```python
class A:
	def __init__(self, x:int, y:int, z:int=1):
		self.x = x
		self.y = y
		self.z = z

	def mymethod(self, m:int) -> int:
		return self.x * m

```
The struct layout of the class above `A` is defined in the construtor method `__init__`.
The named param `z` defaults to 1.
Below an instance of `A` is created and passed to `call_method` through a lambda function,
where `a.mymethod` gets returned and printed.

```python
def call_method( cb:lambda(int)(int), mx:int ) ->int:
	return cb(mx)

```
Callback functions can be passed as arguments to other functions, the type of the argument is given
with this syntax: `name : lambda(A)(R)`, where `A` are the input types, and `R` is the return type.
In the function above `call_method` the first argument `cb` is a lambda function that takes an integer
and returns an integer.

```python
def main():
	a = A( 100, 200, z=9999 )
	print( a.x )
	print( a.y )
	print( a.z )
	b = a.mymethod(3)
	print( b )
	c = call_method( lambda W=int: a.mymethod(W), 4 )
	print( c )

```
Rust and C++ require a lambda function wrapper in order to pass a method as a callback function.
Above the first argument to `call_method` is a special form of lambda where the type of the argument
is given after `=`. The types of input arguments for a lambda function only need to be defined when
translating to C++, because the Rust compiler is able to infer those types automatically. 


translation to Rust
------------
```rust
    /*      class: A        */
    struct A {
        __class__ : string,
        y : int,
        x : int,
        z : int,
    }

    impl A {
        fn __init__(&mut self, x:int, y:int, __kwargs : _kwargs_type_) {
            let mut z = 1;
            if (__kwargs.__use__z == true) {
              z = __kwargs.z;
            }
            self.x = x;
            self.y = y;
            self.z = z;
        }

        fn mymethod(&mut self, m:int) -> int {
            return (self.x * m);
        }

        /*      constructor     */
        fn new( x:int,y:int,__kwargs : _kwargs_type_ ) -> A {
            let mut __ref__ = A{__class__:"A",y:0,x:0,z:0};
            __ref__.__init__(x,y,__kwargs);
            return __ref__; 
        }
    }

    fn call_method(cb:|int|->int, mx:int) -> int {

        return cb(mx);
    }

    fn main() {
        let a : Rc<RefCell<A>> = Rc::new(RefCell::new( A::new(100, 200,_kwargs_type_{z:9999,__use__z:true}) ));
        println!("{}", a.borrow_mut().x);
        println!("{}", a.borrow_mut().y);
        println!("{}", a.borrow_mut().z);
        let mut b = a.borrow_mut().mymethod(3);
        println!("{}", b);
        let c = call_method(|W| a.borrow_mut().mymethod(W) , 4);
        println!("{}", c);
    }

```

translation to C++11
------------
```c++
    /*      class: A        */
    class A {
      public:
        int  y;
        int  x;
        int  z;
        void __init__(int x, int y, _kwargs_type_  __kwargs);
        int mymethod(int m);
        A() {}
    };
    void A::__init__(int x, int y, _kwargs_type_  __kwargs) {

        int  z = 1;
        if (__kwargs.__use__z == true) {
          z = __kwargs.z;
        }
        this->x = x;
        this->y = y;
        this->z = z;
    }
    int A::mymethod(int m) {

        return (this->x * m);
    }

    int call_method(std::function<int(int)>  cb, int mx) {

        return cb(mx);
    }

    int main() {

        A  _ref_a = A{};
        _ref_a.__init__(100, 200,_kwargs_type_{z:9999,__use__z:true});
        std::shared_ptr<A> a = std::make_shared<A>(_ref_a);

        std::cout << a->x << std::endl;
        std::cout << a->y << std::endl;
        std::cout << a->z << std::endl;
        auto b = a->mymethod(3);            /* a  class: A */
        std::cout << b << std::endl;
        auto c = call_method([&](int  W){ return a->mymethod(W); }, 4);         /* new variable */
        std::cout << c << std::endl;
        return 0;
    }
```

ASM Example
===============
Rusthon supports GCC inline assembly using the C++ backend.
This allows you to fully optimize CPU performance, and code directly for bare metal.

Assembly code is given inside a `with asm(...):` indented block.
The syntax is:
```python
with asm( outputs=R, inputs=(...), volatile=True/False, clobber=('cc', 'memory', ...) ):
	movl %1 %%ebx;
	...

```
The `with asm` options follow GCC's extended ASM syntax.
http://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html#s5

Rusthon input
------------

```python
def test_single_input( a : int ) -> int:
	b = 0
	with asm( outputs=b, inputs=a, volatile=True, clobber='%ebx', alignstack=True ):
		movl %1, %%ebx;
		movl %%ebx, %0;
	return b

def test_multi_input( a : int, b : int ) -> int:
	out = 0
	with asm( outputs=out, inputs=(a,b), volatile=True, clobber=('%ebx','memory') ):
		movl %1, %%ebx;
		addl %2, %%ebx;
		movl %%ebx, %0;
	return out


def main():
	x = test_single_input(999)
	print x  ## prints 999
	y = test_multi_input(400, 20)
	print y  ## prints 420
```

C++ output
------------

```c++
int test_single_input(int a) {

	auto   b = 0;
	asm volatile ( "movl %1, %%ebx;movl %%ebx, %0;" : "=r" (b) : "r" (a) : "%ebx" );
	return b;
}
int test_multi_input(int a, int b) {

	auto   out = 0;
	asm volatile ( "movl %1, %%ebx;addl %2, %%ebx;movl %%ebx, %0;" : "=r" (out) : "r" (a),"r" (b) : "%ebx","memory" );
	return out;
}
int main() {

	auto   x = test_single_input(999);
	std::cout << x << std::endl;
	auto   y = test_multi_input(400, 20);
	std::cout << y << std::endl;
	return 0;
}
```