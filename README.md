Introduction
------------
Rusthon is a python-like language that converts and compiles into: Rust, C++, and JavaScript.


Simple Class Example
===============


Rusthon input
------------
```
class A:
	def __init__(self, x:int, y:int, z:int=1):
		let self.x : int = x
		let self.y : int = y
		let self.z : int = z

	def mymethod(self, m:int) -> int:
		return self.x * m

```
The struct layout of the class above `A` is defined in the construtor method `__init__`.


```
def call_method( cb:lambda(int)(int), mx:int ) ->int:
	return cb(mx)

```
Callback functions can be passed as arguments to other functions, the type of the argument is given
with this syntax: `name : lambda(A)(R)`, where `A` are the input types, and `R` is the return type.
In the function above `call_method` the first argument `cb` is a lambda function that takes an integer
and returns an integer.

```
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
```
    struct A {
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
    }

    fn call_method(cb:|int|->int, mx:int) -> int {
     
            return cb(mx);
    }

    fn main() {
     
            let a = &mut A{ y:100,x:200,z:9999 };
            println!("{}", a.x);
            println!("{}", a.y);
            println!("{}", a.z);
            let b = a.mymethod(3);
            println!("{}", b);
            let c = call_method(|W| a.mymethod(W) , 4);
            println!("{}", c);
    }

```

translation to C++11
------------
```
class A {
  public:
        int  y;
        int  x;
        int  z;
        void __init__(int x, int y, _kwargs_type_  __kwargs);
        int mymethod(int m);
        A( int x,int y,_kwargs_type_  __kwargs ) { this->__init__( x,y,__kwargs ); }
};

void A::__init__(int x, int y, _kwargs_type_  __kwargs) {

        int  z = 1;
        if (__kwargs.__use__z == true) {z = __kwargs.z;}
        A self = *this;
        this->x = x;
        this->y = y;
        this->z = z;
}

int A::mymethod(int m) {

        A self = *this;
        return (self.x * m);
}

int call_method(std::function<int(int)>  cb, int mx) {
 
        return cb(mx);
}

int main() {
 
        auto a = new A(100, 200,_kwargs_type_{z:9999,__use__z:true});
        std::cout << a->x << std::endl;
        std::cout << a->y << std::endl;
        std::cout << a->z << std::endl;
        auto b = a->mymethod(3);                  
        std::cout << b << std::endl;
        auto c = call_method([&](int  W){ return a->mymethod(W); }, 4);
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
```
with asm( outputs=R, inputs=(...), volatile=True/False, clobber=('cc', 'memory', ...) ):
	movl %1 %%ebx;
	...

```
The `with asm` options follow GCC's extended ASM syntax.
http://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html#s5

Rusthon input
------------

```
def test_single_input( a : int ) -> int:
	let mut b : int = 0
	with asm( outputs=b, inputs=a, volatile=True, clobber='%ebx', alignstack=True ):
		movl %1, %%ebx;
		movl %%ebx, %0;
	return b

def test_multi_input( a : int, b : int ) -> int:
	let mut out : int = 0
	with asm( outputs=out, inputs=(a,b), volatile=True, clobber=('%ebx','memory') ):
		movl %1, %%ebx;
		addl %2, %%ebx;
		movl %%ebx, %0;
	return out


def main():
	let x : int = test_single_input(999)
	print x  ## prints 999
	let y : int = test_multi_input(400, 20)
	print y  ## prints 420
```

C++ output
------------

```
int test_single_input(int a) {

	int   b = 0;
	asm volatile ( "movl %1, %%ebx;movl %%ebx, %0;" : "=r" (b) : "r" (a) : "%ebx" );
	return b;
}
int test_multi_input(int a, int b) {

	int   out = 0;
	asm volatile ( "movl %1, %%ebx;addl %2, %%ebx;movl %%ebx, %0;" : "=r" (out) : "r" (a),"r" (b) : "%ebx","memory" );
	return out;
}
int main() {

	int   x = test_single_input(999);
	std::cout << x << std::endl;
	int   y = test_multi_input(400, 20);
	std::cout << y << std::endl;
	return 0;
}
```