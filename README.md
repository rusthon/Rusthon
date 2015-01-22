This compiles and runs a project in literate multi-language markdown format.
```
cd Rusthon
./rusthon.py path/to/myproject.md
```
https://github.com/rusthon/Rusthon/blob/master/examples/example-project.md

The option `--tar` can be used to save the source code of the translated code,
javascripts and python scripts inside the markdown, and compiled exes.
```
./rusthon.py myproject.md --tar project.tar
```

Docs
----
https://github.com/rusthon/Rusthon/wiki
https://github.com/rusthon/Rusthon/blob/master/doc/syntax.md
https://github.com/rusthon/Rusthon/blob/master/doc/memory.md
https://github.com/rusthon/Rusthon/blob/master/doc/pythonjs.md


Example
-------
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