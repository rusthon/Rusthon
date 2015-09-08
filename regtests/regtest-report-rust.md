Rust Backend Regression Tests
-----------------------------
the following tests compiled, and the binary executed without any errors
* [chan_universal_style.py](rust/chan_universal_style.py)

input:
------
```python
"""send int over channel for rust, go, and c++"""

def sender_wrapper(a:int, send: chan Sender<int> ):
	result = 100
	send <- result

def recv_wrapper(a:int, recver: chan Receiver<int> ) -> int:
	v = <- recver
	return v

def main():
	## sender and recver are the same object in Go and C++
	sender, recver = channel(int)
	spawn( sender_wrapper(17, sender) )
	# Do other work in the current goroutine until the channel has a result.
	x = recv_wrapper(2, recver)
	print(x)
	assert x==100
```
output:
------
```rust

fn sender_wrapper(a:int, send : Sender<int>) {
	let mut result = 100i64;			/* new muatble */
	send.send(result).unwrap();
}
fn recv_wrapper(a:int, recver : Receiver<int>) -> int {
	let mut v = recver.recv().unwrap();			/* new muatble */
	return v;
}
fn main() {
	let (sender,recver) = channel::<int>();
	thread::spawn( move || {sender_wrapper(17, sender);} );
	let x = recv_wrapper(2, recver);			/* new variable */
	println!("{}", x);
	if (!(( x == 100 ))) {panic!("assertion failed: ( x == 100 )"); }
}
```
* [simple_class.py](rust/simple_class.py)

input:
------
```python
'''
simple class
'''
class A:
	def __init__(self, x:int, y:int, z:int):
		self.x = x
		self.y = y
		self.z = z

	def mymethod(self, m:int) -> int:
		return self.x * m

def call_method( cb:lambda(int)(int), mx:int ) ->int:
	return cb(mx)

def main():
	a = A( 100, 200, 9999 )
	print( a.x )
	print( a.y )
	print( a.z )
	assert a.x == 100

	b = a.mymethod(3)
	print( b )

	## taking the address of a method pointer is not allowed in rust
	## http://stackoverflow.com/questions/24728394/rust-method-pointer
	##c = call_method( a.mymethod, 4 )

	c = call_method( lambda W=int: a.mymethod(W), 4 )
	print( c )
```
output:
------
```rust

struct A {
	__class__ : string,
	y : int,
	x : int,
	z : int,
}
impl A {
	fn __init__(&mut self, x:int, y:int, z:int) {
		self.x = x;
		self.y = y;
		self.z = z;
	}
	fn mymethod(&mut self, m:int) -> int {
		return (self.x * m);
	}
/*		constructor		*/
	fn new( x:int,y:int,z:int ) -> A { let mut __ref__ = A{__class__:"A",y:0,x:0,z:0};__ref__.__init__(x,y,z);return __ref__; }
}
fn call_method<__functype__0>(cb:__functype__0, mx:int) -> int
	where
		__functype__0:Fn(int) ->int,
{
	return cb(mx);
}
fn main() {
	let a : Rc<RefCell<A>> = Rc::new(RefCell::new( A::new(100, 200, 9999) ));
	println!("{}", a.borrow_mut().x);
	println!("{}", a.borrow_mut().y);
	println!("{}", a.borrow_mut().z);
	if (!(( a.borrow_mut().x == 100 ))) {panic!("assertion failed: ( a.borrow_mut().x == 100 )"); }
	let mut b = a.borrow_mut().mymethod(3);			/* a   */
	println!("{}", b);
	let c = call_method(|W| a.borrow_mut().mymethod(W) , 4);			/* new variable */
	println!("{}", c);
}
```
* [arrays.py](rust/arrays.py)

input:
------
```python
"""array types"""

def test_pass_array_as_arg( arr:[]int ):
	#m = arr.borrow_mut()
	#m.push( 5 )
	arr.append( 5 )

def main():
	a = []int(1,2,3)
	assert a[0]==1
	assert len(a)==3
	a.append( 4 )

	assert len(a)==4

	test_pass_array_as_arg( a.clone() )  ## Rc needs to be cloned because `a` is used after this call below.
	assert len(a)==5

	b = [2]int(100,200)
	assert b[0]==100
	assert b[1]==200

	#c = a[:2]
	#TestError( len(c)==2 )

	#d = range(10)
	#TestError(len(d)==10)
	#d.append(99)
	#TestError(len(d)==11)

	#e = range(2,10)
	#TestError(len(e)==8)

	#f = range(2,10, 2)
	#TestError(len(f)==4)
```
output:
------
```rust

fn test_pass_array_as_arg(arr:Rc<RefCell<Vec<int>>>) {
	arr.borrow_mut().push(5);
}
fn main() {
	let a = Rc::new(RefCell::new(vec!(1i64,2i64,3i64)));	/* new array */
	if (!(( a.borrow_mut()[0] == 1 ))) {panic!("assertion failed: ( a.borrow_mut()[0] == 1 )"); }
	if (!(( a.borrow().len() == 3 ))) {panic!("assertion failed: ( a.borrow().len() == 3 )"); }
	a.borrow_mut().push(4);
	if (!(( a.borrow().len() == 4 ))) {panic!("assertion failed: ( a.borrow().len() == 4 )"); }
	test_pass_array_as_arg(a.clone());
	if (!(( a.borrow().len() == 5 ))) {panic!("assertion failed: ( a.borrow().len() == 5 )"); }
	let b = Rc::new(RefCell::new(vec!(100i64,200i64)));	/* new array */
	if (!(( b.borrow_mut()[0] == 100 ))) {panic!("assertion failed: ( b.borrow_mut()[0] == 100 )"); }
	if (!(( b.borrow_mut()[1] == 200 ))) {panic!("assertion failed: ( b.borrow_mut()[1] == 200 )"); }
}
```
* [list_comp.py](rust/list_comp.py)

input:
------
```python
'''
rust list comprehensions
'''
class A:
	def __init__(self, id:int ):
		self.id = id


def test_pass_array( arr:[]int ):
	arr.append( 3 )

# `[]A` for c++11 backend becomes `std::shared_ptr<std::vector<std::shared_ptr<A>>>`
def test_pass_array_of_objects( arr:[]A, id:int ):
	a = A( id )
	arr.append( a )

def main():
	a = []int(x for x in range(3))
	assert len(a)==3
	assert a[0]==0
	assert a[1]==1
	assert a[2]==2

	test_pass_array( a )
	assert len(a)==4
	assert a[3]==3

	#b = []A( A(x) for x in ['list', 'comp'])  ## TODO fix me, infer type

	#stuff = []string('list', 'comp')
	#b = []A( A(x) for x in stuff)
	#b = []A( A(x) for x in ('list', 'comp'))  ## TODO fix strings

	b = []A( A(x) for x in (1,2,3,4))
	assert len(b)==4
	test_pass_array_of_objects( b, 5 )
	assert len(b)==5
```
output:
------
```rust

struct A {
	__class__ : string,
	id : int,
}
impl A {
	fn __init__(&mut self, id:int) {
		self.id = id;
	}
/*		constructor		*/
	fn new( id:int ) -> A { let mut __ref__ = A{__class__:"A",id:0};__ref__.__init__(id);return __ref__; }
}
fn test_pass_array(arr:Rc<RefCell<Vec<int>>>) {
	arr.borrow_mut().push(3);
}
fn test_pass_array_of_objects(arr:Rc<RefCell<Vec<Rc<RefCell<A>>>>>, id:int) {
	let a : Rc<RefCell<A>> = Rc::new(RefCell::new( A::new(id) ));
	arr.borrow_mut().push(a);
}
fn main() {
	let mut _comp_a : Vec<int> = Vec::new();
for x in 0u32..3u32 {
	_comp_a.push(x as int);
}
let a : Rc<RefCell< Vec<int> >> = Rc::new(RefCell::new(_comp_a));
	if (!(( a.borrow().len() == 3 ))) {panic!("assertion failed: ( a.borrow().len() == 3 )"); }
	if (!(( a.borrow_mut()[0] == 0 ))) {panic!("assertion failed: ( a.borrow_mut()[0] == 0 )"); }
	if (!(( a.borrow_mut()[1] == 1 ))) {panic!("assertion failed: ( a.borrow_mut()[1] == 1 )"); }
	if (!(( a.borrow_mut()[2] == 2 ))) {panic!("assertion failed: ( a.borrow_mut()[2] == 2 )"); }
	test_pass_array(a.clone());
	if (!(( a.borrow().len() == 4 ))) {panic!("assertion failed: ( a.borrow().len() == 4 )"); }
	if (!(( a.borrow_mut()[3] == 3 ))) {panic!("assertion failed: ( a.borrow_mut()[3] == 3 )"); }
	let mut _comp_b : Vec< Rc<RefCell<A>> > = Vec::new();
for &x in vec!(1, 2, 3, 4).iter() {
	_comp_b.push(Rc::new(RefCell::new( A::new(x) )));
}
let b : Rc<RefCell< Vec<Rc<RefCell<A>>> >> = Rc::new(RefCell::new(_comp_b));
	if (!(( b.borrow().len() == 4 ))) {panic!("assertion failed: ( b.borrow().len() == 4 )"); }
	test_pass_array_of_objects(b.clone(), 5);
	if (!(( b.borrow().len() == 5 ))) {panic!("assertion failed: ( b.borrow().len() == 5 )"); }
}
```
* [chan.py](rust/chan.py)

input:
------
```python
"""rust send int over channel"""

def sender_wrapper(a:int, send: Sender<int> ):
	result = 100
	send <- result

def recv_wrapper(a:int, recver: Receiver<int> ) -> int:
	v = <- recver
	return v

def main():
	sender, recver = channel(int)
	spawn( sender_wrapper(17, sender) )
	# Do other work in the current goroutine until the channel has a result.
	x = recv_wrapper(2, recver)
	#x = <-recver
	print(x)
	assert x==100
```
output:
------
```rust

fn sender_wrapper(a:int, send:Sender<int>) {
	let mut result = 100i64;			/* new muatble */
	send.send(result).unwrap();
}
fn recv_wrapper(a:int, recver:Receiver<int>) -> int {
	let mut v = recver.recv().unwrap();			/* new muatble */
	return v;
}
fn main() {
	let (sender,recver) = channel::<int>();
	thread::spawn( move || {sender_wrapper(17, sender);} );
	let x = recv_wrapper(2, recver);			/* new variable */
	println!("{}", x);
	if (!(( x == 100 ))) {panic!("assertion failed: ( x == 100 )"); }
}
```
* [multiple_inheritance.py](rust/multiple_inheritance.py)

input:
------
```python
'''
multiple inheritance
'''
class A:
	def foo(self) -> int:
		return 1

class B:
	def bar(self) -> int:
		return 2

class C( A, B ):
	def call_foo_bar(self) -> int:
		let mut a = self.foo()
		a += self.bar()
		return a

	def foo(self) -> int:
		return 100
	def bar(self) -> int:
		return 200

	def test_parents(self) -> int:
		#return A.foo(self) + B.bar(self)  ## this also  works
		return A.foo() + B.bar()


def main():
	a = A()
	assert a.foo()==1
	b = B()
	assert b.bar()==2

	c = C()
	assert c.foo()==100
	assert c.bar()==200

	assert c.call_foo_bar()==300
	assert c.test_parents()==3
```
output:
------
```rust

struct A {
	__class__ : string,
}
impl A {
	fn foo(&mut self, ) -> int {
		return 1;
	}
/*		constructor		*/
	fn new() -> A { let mut __ref__ = A{__class__:"A"};return __ref__; }
}
struct B {
	__class__ : string,
}
impl B {
	fn bar(&mut self, ) -> int {
		return 2;
	}
/*		constructor		*/
	fn new() -> B { let mut __ref__ = B{__class__:"B"};return __ref__; }
}
struct C {
	__class__ : string,
//	members from class: B  []
//	members from class: A  []
}
impl C {
	fn call_foo_bar(&mut self, ) -> int {
		let mut a = self.foo();
		a += self.bar();
		return a;
	}
	fn foo(&mut self, ) -> int {
		return 100;
	}
	fn bar(&mut self, ) -> int {
		return 200;
	}
	fn test_parents(&mut self, ) -> int {
		return (self.__A_foo() + self.__B_bar());
	}
/*		overloaded methods		*/
fn __B_bar(&mut self, ) -> int {
	return 2;
}
fn __A_foo(&mut self, ) -> int {
	return 1;
}
/*		constructor		*/
	fn new() -> C { let mut __ref__ = C{__class__:"C"};return __ref__; }
}
fn main() {
	let a : Rc<RefCell<A>> = Rc::new(RefCell::new( A::new() ));
	if (!(( a.borrow_mut().foo() == 1 ))) {panic!("assertion failed: ( a.borrow_mut().foo() == 1 )"); }
	let b : Rc<RefCell<B>> = Rc::new(RefCell::new( B::new() ));
	if (!(( b.borrow_mut().bar() == 2 ))) {panic!("assertion failed: ( b.borrow_mut().bar() == 2 )"); }
	let c : Rc<RefCell<C>> = Rc::new(RefCell::new( C::new() ));
	if (!(( c.borrow_mut().foo() == 100 ))) {panic!("assertion failed: ( c.borrow_mut().foo() == 100 )"); }
	if (!(( c.borrow_mut().bar() == 200 ))) {panic!("assertion failed: ( c.borrow_mut().bar() == 200 )"); }
	if (!(( c.borrow_mut().call_foo_bar() == 300 ))) {panic!("assertion failed: ( c.borrow_mut().call_foo_bar() == 300 )"); }
	if (!(( c.borrow_mut().test_parents() == 3 ))) {panic!("assertion failed: ( c.borrow_mut().test_parents() == 3 )"); }
}
```
* [simple_subclass.py](rust/simple_subclass.py)

input:
------
```python
'''
simple subclass
'''
class A:
	def __init__(self, x:int, y:int, z:int):
		self.x = x
		self.y = y
		self.z = z

	def mymethod(self, m:int) -> int:
		return self.x * m

class B(A):
	def __init__(self, s:string):
		A.__init__(self, 4, 5, 6)
		let self.w : string = s
		let self.x : int    = 1

	def method2(self, v:string) ->string:
		print(self.x)
		self.w = v
		## returning `self.w` or `v` is not allowed in Rust,
		## because `v` is now owned by `self`
		#return self.w
		return "ok"

def call_method( cb:lambda(int)(int), mx:int ) ->int:
	return cb(mx)

def main():
	a = A( 100, 200, 9999 )
	print( a.x )
	print( a.y )
	print( a.z )

	b = a.mymethod(3)
	print( b )

	c = call_method( lambda W=int: a.mymethod(W), 4 )
	print( c )

	x = B('testing...')
	print( x.method2('hello world') )
	print( x.w )
```
output:
------
```rust

struct A {
	__class__ : string,
	y : int,
	x : int,
	z : int,
}
impl A {
	fn __init__(&mut self, x:int, y:int, z:int) {
		self.x = x;
		self.y = y;
		self.z = z;
	}
	fn mymethod(&mut self, m:int) -> int {
		return (self.x * m);
	}
/*		constructor		*/
	fn new( x:int,y:int,z:int ) -> A { let mut __ref__ = A{__class__:"A",y:0,x:0,z:0};__ref__.__init__(x,y,z);return __ref__; }
}
struct B {
	__class__ : string,
//	members from class: A  ['y', 'x', 'z']
	y : int,
	x : int,
	z : int,
	s : String,
	w : String,
}
impl B {
	fn __init__(&mut self, s:String) {
		self.__A___init__(4, 5, 6);
		self.w = s;
		self.x = 1;
	}
	fn method2(&mut self, v:String) -> String {
		println!("{}", self.x);
		self.w = v;
		return "ok".to_string();
	}
/*		overloaded methods		*/
fn __A___init__(&mut self, x:int, y:int, z:int) {
	self.x = x;
	self.y = y;
	self.z = z;
}
fn mymethod(&mut self, m:int) -> int {
	return (self.x * m);
}
/*		constructor		*/
	fn new( s:String ) -> B { let mut __ref__ = B{__class__:"B",y:0,x:0,z:0,s:"".to_string(),w:"".to_string()};__ref__.__init__(s);return __ref__; }
}
fn call_method<__functype__0>(cb:__functype__0, mx:int) -> int
	where
		__functype__0:Fn(int) ->int,
{
	return cb(mx);
}
fn main() {
	let a : Rc<RefCell<A>> = Rc::new(RefCell::new( A::new(100, 200, 9999) ));
	println!("{}", a.borrow_mut().x);
	println!("{}", a.borrow_mut().y);
	println!("{}", a.borrow_mut().z);
	let mut b = a.borrow_mut().mymethod(3);			/* a   */
	println!("{}", b);
	let c = call_method(|W| a.borrow_mut().mymethod(W) , 4);			/* new variable */
	println!("{}", c);
	let x : Rc<RefCell<B>> = Rc::new(RefCell::new( B::new("testing...".to_string()) ));
	println!("{}", x.borrow_mut().method2("hello world".to_string()));
	println!("{}", x.borrow_mut().w);
}
```