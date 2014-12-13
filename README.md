Introduction
------------
Rusthon is a python-like language that converts and compiles into: Rust, C++, and JavaScript.


Example
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

def call_method( cb:lambda(int)(int), mx:int ) ->int:
	return cb(mx)

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
        auto b = a->mymethod(3);                        /* a  class: A */
        std::cout << b << std::endl;
        auto c = call_method([&](int  W){ return a->mymethod(W); }, 4);                 /* new variable */
        std::cout << c << std::endl;
        return 0;
}
```