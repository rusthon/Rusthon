C++11 Backend Regression Tests
-----------------------------
the following tests compiled, and the binary executed without any errors
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/pointers_returns_array2D.py](pointers_returns_array2D.py)
input:
------
```python
'''
returns array of arrays
'''

with pointers:
	def make_array() -> [][]int:
		arr = new(
			[][]int(
				(1,2,3),
				(4,5,6,7,8)
			)
		)
		return arr

	def test_array( arr:[][]int ):
		print( arr[0][0] )

	def main():
		a = make_array()
		print( len(a))
		print( len(a[0]) )
		print( len(a[1]) )

		test_array(a)
```
output:
------
```c++

std::vector<std::vector<int>*>* make_array() {

	auto arr = (new std::vector<std::vector<int>*> {new std::vector<int> {1,2,3},new std::vector<int> {4,5,6,7,8}});			/* new variable */
	return arr;
}
void test_array(std::vector<std::vector<int>*>* arr) {

	std::cout << (*(*arr)[0])[0] << std::endl;
}
int main() {

	auto a = make_array();			/* new variable */
	std::cout << a->size() << std::endl;
	std::cout << (*a)[0]->size() << std::endl;
	std::cout << (*a)[1]->size() << std::endl;
	test_array(a);
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/pointers_returns_array.py](pointers_returns_array.py)
input:
------
```python
'''
returns array of arrays
'''

with pointers:
	def make_array() -> []int:
		arr = new([]int( 1,2,3,4 ))
		return arr

	def test_array( arr:[]int ):
		print( arr[0] )
		print( arr[1] )
		print( arr[2] )
		print( arr[3] )

	def main():
		a = make_array()
		print('arr length:', len(a))
		test_array(a)
```
output:
------
```c++

std::vector<int>* make_array() {

	auto arr = (new std::vector<int> {1,2,3,4});			/* new variable */
	return arr;
}
void test_array(std::vector<int>* arr) {

	std::cout << (*arr)[0] << std::endl;
	std::cout << (*arr)[1] << std::endl;
	std::cout << (*arr)[2] << std::endl;
	std::cout << (*arr)[3] << std::endl;
}
int main() {

	auto a = make_array();			/* new variable */
	std::cout << std::string("arr length:");
std::cout << a->size();std::cout << std::endl;
	test_array(a);
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/chan.py](chan.py)
input:
------
```python
"""cpp-channel backend - send int over channel"""

def sender_wrapper(a:int, send: chan int ):
	## `chan T` is an alias for `cpp::channel<T>`
	print 'sending'
	result = 100
	send <- result

def recv_wrapper(a:int, recver: cpp::channel<int> ) -> int:
	## above namespace and template are given c++ style to recver
	print 'receiving'
	v = <- recver
	return v

def main():
	print 'enter main'
	c = channel(int)  ## `channel(T)` translates to: `cpp::channel<T>`
	print 'new channel'
	## spawn creates a new std::thread, 
	## and joins it at the end of the function.
	print 'doing spawn thread'
	spawn( sender_wrapper(17, c) )
	print 'done spawning thread'
	# Do other work...
	x = recv_wrapper(2, c)
	print(x)
	assert x==100
	print 'ok'
```
output:
------
```c++

void sender_wrapper(int a, cpp::channel<int>  send) {

	std::cout << std::string("sending") << std::endl;
	auto result = 100;  /* fallback */
	send.send(result);
}
int recv_wrapper(int a, cpp::channel<int> recver) {

	std::cout << std::string("receiving") << std::endl;
	auto v = recver.recv();
	return v;
}
int main() {

	std::cout << std::string("enter main") << std::endl;
	auto c = cpp::channel<int>{};			/* new variable */
	std::cout << std::string("new channel") << std::endl;
	std::cout << std::string("doing spawn thread") << std::endl;
	std::thread __thread0__( [&]{sender_wrapper(17, c);} );
	std::cout << std::string("done spawning thread") << std::endl;
	auto x = recv_wrapper(2, c);			/* new variable */
	std::cout << x << std::endl;
	if (!(( x == 100 ))) {throw std::runtime_error("assertion failed: ( x == 100 )"); }
	std::cout << std::string("ok") << std::endl;
	if (__thread0__.joinable()) __thread0__.join();
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/named_params.py](named_params.py)
input:
------
```python
'''
keyword arguments
'''

def f1( a=1 ) -> int:
	return a*2

## this break rust because the global kwargs-type then requires `b` and `__use__b`
## but the caller only gives `a` and `__use__a`
def f2( a=1, b=2 ) -> int:
	return a + b

def main():
	print( f1(a=100) )
	#print( f2(a=100, b=200) )  ## TODO fix in c++
```
output:
------
```c++

int f1(_KwArgs_*  __kwargs) {

	int  a = 1;
	if (__kwargs->__use__a == true) {
	  a = __kwargs->_a_;
	}
	return (a * 2);
}
int f2(_KwArgs_*  __kwargs) {

	int  a = 1;
	if (__kwargs->__use__a == true) {
	  a = __kwargs->_a_;
	}
	int  b = 2;
	if (__kwargs->__use__b == true) {
	  b = __kwargs->_b_;
	}
	return (a + b);
}
int main() {

	std::cout << f1((new _KwArgs_())->a(100)) << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/array_slice.py](array_slice.py)
input:
------
```python
'''
array slice syntax
'''

def somefunc():
	a = [1,2,3,4,5]
	print('a addr:', a)
	print('len a:', len(a))
	b = a[1:]
	print('b addr (should not be `a` above):', b)
	print('len b  (should be 4):', len(b))

	c = a[:]
	print('c addr (should not be `a` or `b` above):', c)
	print('len c:', len(c))
	c.append(6)
	print('len c - after append:', len(c))
	print('len a:', len(a))

	print('end slice test')

	d = a[:2]
	print('len d:', len(d))
	print d[0]
	print d[1]

	print('len a:', len(a))
	e = a[::1]
	print('len e should be same as a:', len(e))
	for i in e: print i

	f = a[::2]
	print('len f:', len(f))
	for i in f: print i

	g = a[::-1]
	print('len g:', len(g))
	for i in g: print i

	h = a[2::-1]
	print('len h:', len(h))
	for i in h: print i

	print('---slice assignment---')
	h.append(1000)
	h.append(1000)
	a[:2] = h
	for i in a: print i
	print('len a:', len(a))

	print('somefunc done')

def main():
	print('calling somefunc')
	somefunc()

	## never reached because there is a segfault at the end
	## of somefunc when the slices go out of scope, they are free'ed twice.
	print('OK')
```
output:
------
```c++

void somefunc() {

	std::shared_ptr<std::vector<int>> a( (new std::vector<int>({1,2,3,4,5})) ); /* 1D Array */
	std::cout << std::string("a addr:");
std::cout << a;std::cout << std::endl;
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	/* <slice> 1 : None : None */
std::vector<int> _ref_b(
a->begin()+1,
a->end()
);
std::shared_ptr<std::vector<int>> b = std::make_shared<std::vector<int>>(_ref_b);
	std::cout << std::string("b addr (should not be `a` above):");
std::cout << b;std::cout << std::endl;
	std::cout << std::string("len b  (should be 4):");
std::cout << b->size();std::cout << std::endl;
	/* <slice> None : None : None */
std::vector<int> _ref_c(
a->begin(),
a->end()
);
std::shared_ptr<std::vector<int>> c = std::make_shared<std::vector<int>>(_ref_c);
	std::cout << std::string("c addr (should not be `a` or `b` above):");
std::cout << c;std::cout << std::endl;
	std::cout << std::string("len c:");
std::cout << c->size();std::cout << std::endl;
	c->push_back(6);
	std::cout << std::string("len c - after append:");
std::cout << c->size();std::cout << std::endl;
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	std::cout << std::string("end slice test") << std::endl;
	/* <slice> None : 2 : None */
std::vector<int> _ref_d(
a->begin(),
a->begin()+2
);
std::shared_ptr<std::vector<int>> d = std::make_shared<std::vector<int>>(_ref_d);
	std::cout << std::string("len d:");
std::cout << d->size();std::cout << std::endl;
	std::cout << (*d)[0] << std::endl;
	std::cout << (*d)[1] << std::endl;
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	/* <slice> None : None : 1 */
std::vector<int> _ref_e;
if(1<0){for(int _i_=a->size()-1;_i_>=0;_i_+=1){ _ref_e.push_back((*a)[_i_]);}} else {for(int _i_=0;_i_<a->size();_i_+=1){ _ref_e.push_back((*a)[_i_]);}}
std::shared_ptr<std::vector<int>> e = std::make_shared<std::vector<int>>(_ref_e);
	std::cout << std::string("len e should be same<<__as__<<a:");
std::cout << e->size();std::cout << std::endl;
	for (auto &i: (*e)) {
		std::cout << i << std::endl;
	}
	/* <slice> None : None : 2 */
std::vector<int> _ref_f;
if(2<0){for(int _i_=a->size()-1;_i_>=0;_i_+=2){ _ref_f.push_back((*a)[_i_]);}} else {for(int _i_=0;_i_<a->size();_i_+=2){ _ref_f.push_back((*a)[_i_]);}}
std::shared_ptr<std::vector<int>> f = std::make_shared<std::vector<int>>(_ref_f);
	std::cout << std::string("len f:");
std::cout << f->size();std::cout << std::endl;
	for (auto &i: (*f)) {
		std::cout << i << std::endl;
	}
	/* <slice> None : None : -1 */
std::vector<int> _ref_g;
if(-1<0){for(int _i_=a->size()-1;_i_>=0;_i_+=-1){ _ref_g.push_back((*a)[_i_]);}} else {for(int _i_=0;_i_<a->size();_i_+=-1){ _ref_g.push_back((*a)[_i_]);}}
std::shared_ptr<std::vector<int>> g = std::make_shared<std::vector<int>>(_ref_g);
	std::cout << std::string("len g:");
std::cout << g->size();std::cout << std::endl;
	for (auto &i: (*g)) {
		std::cout << i << std::endl;
	}
	/* <slice> 2 : None : -1 */
std::vector<int> _ref_h;
if(-1<0){for(int _i_=a->size()-2-1;_i_>=0;_i_+=-1){ _ref_h.push_back((*a)[_i_]);}} else {for(int _i_=2;_i_<a->size();_i_+=-1){ _ref_h.push_back((*a)[_i_]);}}
std::shared_ptr<std::vector<int>> h = std::make_shared<std::vector<int>>(_ref_h);
	std::cout << std::string("len h:");
std::cout << h->size();std::cout << std::endl;
	for (auto &i: (*h)) {
		std::cout << i << std::endl;
	}
	std::cout << std::string("---slice assignment---") << std::endl;
	h->push_back(1000);
	h->push_back(1000);
	a->erase(a->begin(), a->begin()+2);
a->insert(a->begin(), h->begin(), h->end());
	for (auto &i: (*a)) {
		std::cout << i << std::endl;
	}
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	std::cout << std::string("somefunc done") << std::endl;
}
int main() {

	std::cout << std::string("calling somefunc") << std::endl;
	somefunc();
	std::cout << std::string("OK") << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/print_classname.py](print_classname.py)
input:
------
```python
'''
returns subclasses
'''
class A:
	def __init__(self, x:int):
		self.x = x

	def method(self) -> int:
		return self.x

class B(A):

	def foo(self) ->int:
		return self.x * 2

class C(A):

	def bar(self) ->int:
		return self.x + 200


def main():
	a = A(0)
	b = B(1)
	c = C(2)
	print(a.getclassname())
	print(b.getclassname())
	print(c.getclassname())


```
output:
------
```c++

class A {
  public:
	std::string __class__;
	int  x;
	A* __init__(int x);
	int method();
	A() {__class__ = std::string("A");}
	std::string getclassname() {return this->__class__;}
};
class B:  public A {
  public:
//	members from class: A  ['x']
	int foo();
	B* __init__(int x);
	B() {__class__ = std::string("B");}
	std::string getclassname() {return this->__class__;}
};
class C:  public A {
  public:
//	members from class: A  ['x']
	int bar();
	C* __init__(int x);
	C() {__class__ = std::string("C");}
	std::string getclassname() {return this->__class__;}
};
	C* C::__init__(int x) {

		this->x = x;
		return this;
	}
	int C::bar() {

		return (this->x + 200);
	}
	B* B::__init__(int x) {

		this->x = x;
		return this;
	}
	int B::foo() {

		return (this->x * 2);
	}
	int A::method() {

		return this->x;
	}
	A* A::__init__(int x) {

		this->x = x;
		return this;
	}
int main() {

	auto a = std::shared_ptr<A>((new A())->__init__(0)); // new style
	auto b = std::shared_ptr<B>((new B())->__init__(1)); // new style
	auto c = std::shared_ptr<C>((new C())->__init__(2)); // new style
	std::cout << a->getclassname() << std::endl;
	std::cout << b->getclassname() << std::endl;
	std::cout << c->getclassname() << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/array_sized.py](array_sized.py)
input:
------
```python
'''
array with default size
'''

class A:
	pass

def somefunc():
	a = [5]int(1,2,3,4,5)
	print('len a:', len(a))
	a.pop()
	print('len a:', len(a))
	print(a[0])
	print(a[1])

	b = [10]int()
	print('len b:', len(b))
	print b[0]
	print b[1]

	c = [10]f64( 1.1, 2.2, 3.3 )
	print c[0]
	print c[1]
	print c[2]

	x = A()
	y = A()
	d = [4]A( x,y )
	print d[0]
	print d[1]

def main():
	somefunc()
	print('OK')
```
output:
------
```c++

class A {
  public:
	std::string __class__;
	A() {__class__ = std::string("A");}
	std::string getclassname() {return this->__class__;}
};
void somefunc() {

	std::vector<int> _ref_a = {1,2,3,4,5};_ref_a.resize(5);std::shared_ptr<std::vector<int>> a = std::make_shared<std::vector<int>>(_ref_a);
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	a->pop_back();
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	std::cout << (*a)[0] << std::endl;
	std::cout << (*a)[1] << std::endl;
	std::vector<int> _ref_b = {};_ref_b.resize(10);std::shared_ptr<std::vector<int>> b = std::make_shared<std::vector<int>>(_ref_b);
	std::cout << std::string("len b:");
std::cout << b->size();std::cout << std::endl;
	std::cout << (*b)[0] << std::endl;
	std::cout << (*b)[1] << std::endl;
	std::vector<f64> _ref_c = {1.1,2.2,3.3};_ref_c.resize(10);std::shared_ptr<std::vector<f64>> c = std::make_shared<std::vector<f64>>(_ref_c);
	std::cout << (*c)[0] << std::endl;
	std::cout << (*c)[1] << std::endl;
	std::cout << (*c)[2] << std::endl;
	auto x = std::shared_ptr<A>(new A()); // new style
	auto y = std::shared_ptr<A>(new A()); // new style
	std::vector<std::shared_ptr<A>> _ref_d = {x,y};_ref_d.resize(4);std::shared_ptr<std::vector<std::shared_ptr<A>>> d = std::make_shared<std::vector<std::shared_ptr<A>>>(_ref_d);
	std::cout << (*d)[0] << std::endl;
	std::cout << (*d)[1] << std::endl;
}
int main() {

	somefunc();
	std::cout << std::string("OK") << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/generics.py](generics.py)
input:
------
```python
'''
generic functions
'''

def myfunc( x:int ):
	print( x * 100 )

def myfunc( x:string ):
	print( x + 'world' )

def main():
	myfunc( 10 )
	myfunc( 'hello' )
```
output:
------
```c++

void myfunc(int x) {

	std::cout << (x * 100) << std::endl;
}
void myfunc(std::string x) {

	std::cout << (x + std::string("world")) << std::endl;
}
int main() {

	myfunc(10);
	myfunc(std::string("hello"));
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/classmethod.py](classmethod.py)
input:
------
```python
'''
class methods
'''
class A:
	def __init__(self, x:int, y:int):
		self.x = x
		self.y = y

	@classmethod
	def foo(self):
		print('my classmethod')

	@classmethod
	def bar(self, a:int) ->int:
		return a+1000

def main():
	x = A(1,2)
	x.foo()
	A.foo()
	print x.bar( 100 )
	y = A.bar(200)
	print(y)
```
output:
------
```c++

class A {
  public:
	std::string __class__;
	int  y;
	int  x;
	A* __init__(int x, int y);
	static void foo();
	static int bar(int a);
	A() {__class__ = std::string("A");}
	std::string getclassname() {return this->__class__;}
};
	int A::bar(int a) {

		return (a + 1000);
	}
	void A::foo() {

		std::cout << std::string("my classmethod") << std::endl;
	}
	A* A::__init__(int x, int y) {

		this->x = x;
		this->y = y;
		return this;
	}
int main() {

	auto x = std::shared_ptr<A>((new A())->__init__(1, 2)); // new style
	x->foo();
	A::foo();
	std::cout << x->bar(100) << std::endl;
	auto y = A::bar(200);			/* A   */
	std::cout << y << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/listcomp.py](listcomp.py)
input:
------
```python
'''
list comprehension
'''


def main():
	a = []int( x*2 for x in range(10) )
	print(len(a))
	for item in a:
		print(item)

	## TODO fix slice copy:
	## *** Error in `/tmp/listcomp': free(): invalid pointer: 0x000000000216d218 ***
	#b = [][]int( a[:] for i in range(4)	)
	#print(len(b))
	#print(b[0])
	#print(b[1])
	#print(b[2])
	#print(b[3])
```
output:
------
```c++

int main() {

	std::vector<int> _comp_a;
for (int x=0; x<10; x++) {
	_comp_a.push_back((x * 2));
}
auto a = std::make_shared<std::vector<int>>(_comp_a);
	std::cout << a->size() << std::endl;
	for (auto &item: *a) {
		std::cout << item << std::endl;
	}
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/while.py](while.py)
input:
------
```python
'''
simple while loops
'''


def main():
	i = 10
	while i > 0:
		i -= 1

	print(i)
```
output:
------
```c++

int main() {

	auto i = 10;  /* fallback */
	while (( i > 0 )) {
		i --;
	}
	std::cout << i << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/globals.py](globals.py)
input:
------
```python
'''
simple globals
'''

class A: pass

let a : A = None
b = 0

def check_globals():
	print('a addr:', a)  ## should not print `0`
	print('b value:', b)

def main():
	global a, b
	check_globals()
	a = A()
	print(a)
	print(a.__class__)
	b = 100
	check_globals()
```
output:
------
```c++

class A {
  public:
	std::string __class__;
	A() {__class__ = std::string("A");}
	std::string getclassname() {return this->__class__;}
};
std::shared_ptr<A>  a = nullptr;
int b = 0;
void check_globals() {

	std::cout << std::string("a addr:");
std::cout << a;std::cout << std::endl;
	std::cout << std::string("b value:");
std::cout << b;std::cout << std::endl;
}
int main() {

	check_globals();
	a = std::shared_ptr<A>(new A());
	std::cout << a << std::endl;
	std::cout << a->__class__ << std::endl;
	b = 100;
	check_globals();
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/array_of_arrays.py](array_of_arrays.py)
input:
------
```python
'''
array of arrays
'''

def main():
	## variable size vector of vectors,
	## None is allowed as a sub-vector because each sub-vector is wrapped by std::shared_ptr
	arr = [][]int(
		(1,2,3),
		(4,5,6,7,8),
		None,
		#(x*x for x in range(4)),  ## TODO fix listcomps
		(x for x in range(20)),
	)
	print( len(arr))
	print( len(arr[0]) )
	print( len(arr[1]) )
	if arr[2] is None:
		print('nullptr works ok!')
	else:
		print('never reached')

	print('sub 0 items:')
	for i in arr[0]:
		print( i )

	print('sub 1 items:')
	sub = arr[1]
	for i in sub:
		print(i)

	print('sub 3 items:')
	for i in arr[3]:
		print(i)

	print('sub 3 items changed:')
	arr[3][0] = 1000
	arr[3][1] = 1001
	arr[3][2] = 1002
	arr[3][3] = 1003
	for i in arr[3]:
		print(i)
```
output:
------
```c++

int main() {

	/* arr = vector of vectors to: int */	
std::vector<int> _r__sub0_arr = {1,2,3};	
std::shared_ptr<std::vector<int>> _sub0_arr = std::make_shared<std::vector<int>>(_r__sub0_arr);	
std::vector<int> _r__sub1_arr = {4,5,6,7,8};	
std::shared_ptr<std::vector<int>> _sub1_arr = std::make_shared<std::vector<int>>(_r__sub1_arr);	
std::vector<int> _comp__subcomp_arr;
for (int x=0; x<20; x++) {
	_comp__subcomp_arr.push_back(x);
}
auto _subcomp_arr = std::make_shared<std::vector<int>>(_comp__subcomp_arr);	
std::vector< std::shared_ptr<std::vector<int>> > _ref_arr = {_sub0_arr,_sub1_arr,nullptr,_subcomp_arr};	
std::shared_ptr<std::vector< std::shared_ptr<std::vector<int>> >> arr = std::make_shared<std::vector< std::shared_ptr<std::vector<int>> >>(_ref_arr);
	std::cout << arr->size() << std::endl;
	std::cout << (*arr)[0]->size() << std::endl;
	std::cout << (*arr)[1]->size() << std::endl;
	if (( (*arr)[2] == nullptr )) {
		std::cout << std::string("nullptr works ok!") << std::endl;
	} else {
		std::cout << std::string("never reached") << std::endl;
	}
	std::cout << std::string("sub 0 items:") << std::endl;
	for (auto &i: *(*arr)[0]) {
		std::cout << i << std::endl;
	}
	std::cout << std::string("sub 1 items:") << std::endl;
	auto sub = (*arr)[1];  /* fallback */
	for (auto &i: *sub) {
		std::cout << i << std::endl;
	}
	std::cout << std::string("sub 3 items:") << std::endl;
	for (auto &i: *(*arr)[3]) {
		std::cout << i << std::endl;
	}
	std::cout << std::string("sub 3 items changed:") << std::endl;
	(*(*arr)[3])[0] = 1000;
	(*(*arr)[3])[1] = 1001;
	(*(*arr)[3])[2] = 1002;
	(*(*arr)[3])[3] = 1003;
	for (auto &i: *(*arr)[3]) {
		std::cout << i << std::endl;
	}
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/returns_object.py](returns_object.py)
input:
------
```python
'''
return a class instance
'''
with pointers:
	class A:
		def __init__(self, x:int, y:int):
			self.x = x
			self.y = y

	def create_A() -> A:
		#a = A(1,2)  ## not valid because `a` gets free`ed when function exists
		a = new A(1,2)  ## using `new` the user must manually free the object later
		return a

	def main():
		x = create_A()
		print(x)
		print(x.x)
		print(x.y)
```
output:
------
```c++

class A {
  public:
	std::string __class__;
	int  y;
	int  x;
	A* __init__(int x, int y);
	A() {__class__ = std::string("A");}
	std::string getclassname() {return this->__class__;}
};
A* create_A() {

	auto a = (new A)->__init__(1,2);  /* fallback */
	return a;
}
	A* A::__init__(int x, int y) {

		this->x = x;
		this->y = y;
		return this;
	}
int main() {

	auto x = create_A();			/* new variable */
	std::cout << x << std::endl;
	std::cout << __pointer__(x)->x << std::endl;
	std::cout << __pointer__(x)->y << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/array_slice_assignment.py](array_slice_assignment.py)
input:
------
```python
'''
array slice assignment syntax
'''

def somefunc():
	a = [1,2,3,4,5]
	b = [6,7,8,9,10]
	print('len a:', len(a))
	for i in a:
		print i

	a[:2] = b
	print('len a:', len(a))
	for i in a: print i


def main():
	somefunc()
```
output:
------
```c++

void somefunc() {

	std::shared_ptr<std::vector<int>> a( (new std::vector<int>({1,2,3,4,5})) ); /* 1D Array */
	std::shared_ptr<std::vector<int>> b( (new std::vector<int>({6,7,8,9,10})) ); /* 1D Array */
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	for (auto &i: (*a)) {
		std::cout << i << std::endl;
	}
	a->erase(a->begin(), a->begin()+2);
a->insert(a->begin(), b->begin(), b->end());
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	for (auto &i: (*a)) {
		std::cout << i << std::endl;
	}
}
int main() {

	somefunc();
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/cyclic.py](cyclic.py)
input:
------
```python
'''
detect cyclic parent/child, and insert weakref
'''
class Parent:
	def __init__(self, y:int, children:[]Child ):
		self.children = children
		self.y = y

	def create_child(self, x:int, parent:Parent) ->Child:
		child = Child(x, parent)
		self.children.push_back( child )
		return child

	def say(self, msg:string):
		print(msg)

class Child:
	def __init__(self, x:int, parent:Parent ):
		self.x = x
		self.parent = parent

	def foo(self) ->int:
		'''
		It is also valid to use `par=self.parent`,
		but it is more clear to use `weakref.unwrap(self.parent)`
		'''
		par = weak.unwrap(self.parent)
		if par is not None:
			return self.x * par.y
		else:
			print('parent is gone..')

	def bar(self):
		'''
		below `self.parent` is directly used in expressions,
		and not first assigned to a variable.
		for each use of self.parent the weakref will be promoted
		to a shared pointer, and then fall out of scope, 
		which is slower than above.
		'''
		self.parent.say('hello parent')
		print(self.parent.y)


def main():
	#children = []Child(None,None)
	children = []Child()
	p = Parent( 1000, children )
	print 'parent:', p

	c1 = p.create_child(1, p)
	c2 = p.create_child(2, p)
	c3 = p.create_child(3, p)
	print 'children:'
	print c1
	print c2
	print c3
```
output:
------
```c++

class Parent {
  public:
	std::string __class__;
	int  y;
	std::shared_ptr<std::vector<std::shared_ptr<Child>>>  children;
	Parent* __init__(int y, std::shared_ptr<std::vector<std::shared_ptr<Child>>> children);
	std::shared_ptr<Child> create_child(int x, std::shared_ptr<Parent> parent);
	void say(std::string msg);
	Parent() {__class__ = std::string("Parent");}
	std::string getclassname() {return this->__class__;}
};
class Child {
  public:
	std::string __class__;
	int  x;
	std::weak_ptr<Parent>  parent;
	Child* __init__(int x, std::shared_ptr<Parent> parent);
	int foo();
	void bar();
	Child() {__class__ = std::string("Child");}
	std::string getclassname() {return this->__class__;}
};
/**
 * 
 * 		below `self.parent` is directly used in expressions,
 * 		and not first assigned to a variable.
 * 		for each use of self.parent the weakref will be promoted
 * 		to a shared pointer, and then fall out of scope, 
 * 		which is slower than above.
 * 		
 */
	void Child::bar() {

		__shared__(this->parent.lock())->say(std::string("hello parent"));
		std::cout << __shared__(this->parent.lock())->y << std::endl;
	}
/**
 * 
 * 		It is also valid to use `par=self.parent`,
 * 		but it is more clear to use `weakref.unwrap(self.parent)`
 * 		
 */
	int Child::foo() {

		auto par = this->parent.lock();			/* weak   */
		if (( par != nullptr )) {
			return (this->x * __shared__(par)->y);
		} else {
			std::cout << std::string("parent is gone..") << std::endl;
		}
	}
	Child* Child::__init__(int x, std::shared_ptr<Parent> parent) {

		this->x = x;
		this->parent = parent;
		return this;
	}
	void Parent::say(std::string msg) {

		std::cout << msg << std::endl;
	}
	std::shared_ptr<Child> Parent::create_child(int x, std::shared_ptr<Parent> parent) {

		auto child = std::shared_ptr<Child>((new Child())->__init__(x, parent)); // new style
		__shared__(this->children)->push_back(child);
		return child;
	}
	Parent* Parent::__init__(int y, std::shared_ptr<std::vector<std::shared_ptr<Child>>> children) {

		this->children = children;
		this->y = y;
		return this;
	}
int main() {

	std::shared_ptr<std::vector<std::shared_ptr<Child>>> children( ( new std::vector<std::shared_ptr<Child>>({}) ) ); /* 1D Array */
	auto p = std::shared_ptr<Parent>((new Parent())->__init__(1000, children)); // new style
	std::cout << std::string("parent:");
std::cout << p;std::cout << std::endl;
	auto c1 = p->create_child(1, p);			/* p   */
	auto c2 = p->create_child(2, p);			/* p   */
	auto c3 = p->create_child(3, p);			/* p   */
	std::cout << std::string("children:") << std::endl;
	std::cout << c1 << std::endl;
	std::cout << c2 << std::endl;
	std::cout << c3 << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/array_methods.py](array_methods.py)
input:
------
```python
'''
array methods: append, pop, etc.
'''

def somefunc():
	a = []int(1,2,3,4,5)
	print('len a:', len(a))
	b = a.pop()
	#b = a[len(a)-1]
	a.pop()
	print('len a:', len(a))
	print(b)
	a.insert(0, 1000)
	print('len a:', len(a))
	print(a[0])

def main():
	somefunc()
	print('OK')
```
output:
------
```c++

void somefunc() {

	std::shared_ptr<std::vector<int>> a( (new std::vector<int>({1,2,3,4,5})) ); /* 1D Array */
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	auto b = (*a)[0];
a->erase(a->begin(),a->begin());
	a->pop_back();
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	std::cout << b << std::endl;
	a->insert(a->begin()+0, 1000);
	std::cout << std::string("len a:");
std::cout << a->size();std::cout << std::endl;
	std::cout << (*a)[0] << std::endl;
}
int main() {

	somefunc();
	std::cout << std::string("OK") << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/generics_array_subclasses.py](generics_array_subclasses.py)
input:
------
```python
'''
generics classes with common base.
'''
class A:
	def __init__(self, x:int):
		self.x = x

	def method1(self) -> int:
		return self.x
	def getname(self) -> string:
		return self.__class__

class B(A):
	def method1(self) ->int:
		return self.x * 2
	def method2(self, y:int):
		print( self.x + y )

class C(A):
	def method1(self) ->int:
		return self.x + 200

	def say_hi(self):
		print('hi from C')


def my_generic( g:A ) ->int:
	return g.method1()


def main():
	a = A( 1 )
	b = B( 200 )
	c = C( 3000 )

	print(a.__class__)
	print(b.__class__)
	print(c.__class__)
	print('- - - - - - -')

	arr = []A( a,b,c )
	for item in arr:
		## just prints 100's because c++ runtime method dispatcher thinks item
		## is of class type `A`
		print(item.__class__)
		print( my_generic(item) )

	print('- - - - - - -')

	for item in arr:
		print(item.getname())
		print(item.x)

		## to get to the real subclasses, we need if-isinstance
		if isinstance(item, B):
			print('item is B')
			item.method2( 20 )

		if isinstance(item, C):
			print('item is C')
			item.say_hi()

```
output:
------
```c++

class A {
  public:
	std::string __class__;
	int  x;
	A* __init__(int x);
	int method1();
	std::string getname();
	A() {__class__ = std::string("A");}
	std::string getclassname() {return this->__class__;}
};
class B:  public A {
  public:
//	members from class: A  ['x']
	int method1();
	void method2(int y);
	B* __init__(int x);
	B() {__class__ = std::string("B");}
	std::string getclassname() {return this->__class__;}
};
class C:  public A {
  public:
//	members from class: A  ['x']
	int method1();
	void say_hi();
	C* __init__(int x);
	C() {__class__ = std::string("C");}
	std::string getclassname() {return this->__class__;}
};
int my_generic(std::shared_ptr<A> g) {

	return __shared__(g)->method1();
}
	C* C::__init__(int x) {

		this->x = x;
		return this;
	}
	void C::say_hi() {

		std::cout << std::string("hi from C") << std::endl;
	}
	int C::method1() {

		return (this->x + 200);
	}
	B* B::__init__(int x) {

		this->x = x;
		return this;
	}
	void B::method2(int y) {

		std::cout << (this->x + y) << std::endl;
	}
	int B::method1() {

		return (this->x * 2);
	}
	std::string A::getname() {

		return this->__class__;
	}
	int A::method1() {

		return this->x;
	}
	A* A::__init__(int x) {

		this->x = x;
		return this;
	}
int main() {

	auto a = std::shared_ptr<A>((new A())->__init__(1)); // new style
	auto b = std::shared_ptr<B>((new B())->__init__(200)); // new style
	auto c = std::shared_ptr<C>((new C())->__init__(3000)); // new style
	std::cout << a->__class__ << std::endl;
	std::cout << b->__class__ << std::endl;
	std::cout << c->__class__ << std::endl;
	std::cout << std::string("- - - - - - -") << std::endl;
	std::shared_ptr<std::vector<std::shared_ptr<A>>> arr( ( new std::vector<std::shared_ptr<A>>({a,b,c}) ) ); /* 1D Array */
	for (auto &item: (*arr)) {
		std::cout << __shared__(item)->__class__ << std::endl;
		std::cout << my_generic(item) << std::endl;
	}
	std::cout << std::string("- - - - - - -") << std::endl;
	for (auto &item: (*arr)) {
		std::cout << __shared__(item)->getname() << std::endl;
		std::cout << __shared__(item)->x << std::endl;
		if ((item->__class__==std::string("B"))) {
			auto _cast_item = std::static_pointer_cast<B>(item);
			std::cout << std::string("item is B") << std::endl;
			__shared__(_cast_item)->method2(20);
		}
		if ((item->__class__==std::string("C"))) {
			auto _cast_item = std::static_pointer_cast<C>(item);
			std::cout << std::string("item is C") << std::endl;
			__shared__(_cast_item)->say_hi();
		}
	}
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/subscript.py](subscript.py)
input:
------
```python
'''
simple subscript
'''


def main():
	a = []int(1,2,3)
	index = 0
	a[ index ] = 100
	print(a[index])

	s = "hello world"
	print(s)
	print(s[0])
	print(s[1])
	print(s[2])
	print(s[3])
	if s[0]=='h':
		print('ok')
	else:
		print('error')
```
output:
------
```c++

int main() {

	std::shared_ptr<std::vector<int>> a( (new std::vector<int>({1,2,3})) ); /* 1D Array */
	auto index = 0;  /* fallback */
	(*a)[index] = 100;
	std::cout << (*a)[index] << std::endl;
	auto s = std::string("hello world");  /* fallback */
	std::cout << s << std::endl;
	std::cout << s.substr(0,1) << std::endl;
	std::cout << s.substr(1,1) << std::endl;
	std::cout << s.substr(2,1) << std::endl;
	std::cout << s.substr(3,1) << std::endl;
	if (( s.substr(0,1) == std::string("h") )) {
		std::cout << std::string("ok") << std::endl;
	} else {
		std::cout << std::string("error") << std::endl;
	}
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/returns_subclasses.py](returns_subclasses.py)
input:
------
```python
'''
returns subclasses
'''
class A:
	def __init__(self, x:int):
		self.x = x
	def method(self) -> int:
		return self.x

class B(A):
	def foo(self) ->int:
		return self.x * 2

class C(A):
	def bar(self) ->int:
		return self.x + 200

class D(C):
	def hey(self) ->int:
		return self.x + 1


def some_subclass( x:int ) ->A:
	switch x:
		case 0:
			a = A(1)
			return a
		case 1:
			b = B(2)
			return b
		case 2:
			c = C(3)
			return c
		case 3:
			d = D(4)
			return d


def main():
	a = some_subclass(0)
	b = some_subclass(1)
	c = some_subclass(2)
	d = some_subclass(3)

	print(a.getclassname())
	print(b.getclassname())
	print(c.getclassname())
	print(d.getclassname())

	print(a.method())
	print a.x
	print(b.method())
	print b.x
	print(c.method())
	print c.x
	print(d.method())
	print d.x

	print('- - - - - - - ')
	if isinstance(b, B):
		print('b is type B')
		print(b.method())
		print(b.foo())
	else:
		print('error: b is not type B')

	if isinstance(c, C):
		print('c is type C')
		print(c.method())
		print(c.bar())
	else:
		print('error: c is not type C')

	if isinstance(d, D):
		print('d is type D')
		#print(d.bar())  ## TODO, subclass from C.
		print(d.hey())
	else:
		print('error: d is not type D')

	print('------------------')
	for i in range(3):
		o = some_subclass(i)
		print(o.method())
		if isinstance(o, B):
			print(o.foo())
		if isinstance(o,C):		## TODO-FIX elif isinstance(o,C)
			print(o.bar())

	print('end of test')
```
output:
------
```c++

class A {
  public:
	std::string __class__;
	int  x;
	A* __init__(int x);
	int method();
	A() {__class__ = std::string("A");}
	std::string getclassname() {return this->__class__;}
};
class B:  public A {
  public:
//	members from class: A  ['x']
	int foo();
	B* __init__(int x);
	B() {__class__ = std::string("B");}
	std::string getclassname() {return this->__class__;}
};
class C:  public A {
  public:
//	members from class: A  ['x']
	int bar();
	C* __init__(int x);
	C() {__class__ = std::string("C");}
	std::string getclassname() {return this->__class__;}
};
class D:  public C {
  public:
//	members from class: A  ['x']
	int hey();
	D* __init__(int x);
	D() {__class__ = std::string("D");}
	std::string getclassname() {return this->__class__;}
};
std::shared_ptr<A> some_subclass(int x) {

		switch (x) {
		case 0: {
	auto a = std::shared_ptr<A>((new A())->__init__(1)); // new style
	return a;
	} break;
		case 1: {
	auto b = std::shared_ptr<B>((new B())->__init__(2)); // new style
	return b;
	} break;
		case 2: {
	auto c = std::shared_ptr<C>((new C())->__init__(3)); // new style
	return c;
	} break;
		case 3: {
	auto d = std::shared_ptr<D>((new D())->__init__(4)); // new style
	return d;
	} break;
	}
}
	D* D::__init__(int x) {

		this->x = x;
		return this;
	}
	int D::hey() {

		return (this->x + 1);
	}
	C* C::__init__(int x) {

		this->x = x;
		return this;
	}
	int C::bar() {

		return (this->x + 200);
	}
	B* B::__init__(int x) {

		this->x = x;
		return this;
	}
	int B::foo() {

		return (this->x * 2);
	}
	int A::method() {

		return this->x;
	}
	A* A::__init__(int x) {

		this->x = x;
		return this;
	}
int main() {

	auto a = some_subclass(0);			/* new variable */
	auto b = some_subclass(1);			/* new variable */
	auto c = some_subclass(2);			/* new variable */
	auto d = some_subclass(3);			/* new variable */
	std::cout << __shared__(a)->getclassname() << std::endl;
	std::cout << __shared__(b)->getclassname() << std::endl;
	std::cout << __shared__(c)->getclassname() << std::endl;
	std::cout << __shared__(d)->getclassname() << std::endl;
	std::cout << __shared__(a)->method() << std::endl;
	std::cout << __shared__(a)->x << std::endl;
	std::cout << __shared__(b)->method() << std::endl;
	std::cout << __shared__(b)->x << std::endl;
	std::cout << __shared__(c)->method() << std::endl;
	std::cout << __shared__(c)->x << std::endl;
	std::cout << __shared__(d)->method() << std::endl;
	std::cout << __shared__(d)->x << std::endl;
	std::cout << std::string("- - - - - - - ") << std::endl;
	if ((b->__class__==std::string("B"))) {
		auto _cast_b = std::static_pointer_cast<B>(b);
		std::cout << std::string("b is type B") << std::endl;
		std::cout << __shared__(_cast_b)->method() << std::endl;
		std::cout << __shared__(_cast_b)->foo() << std::endl;
	} else {
		std::cout << std::string("error: b is not type B") << std::endl;
	}
	if ((c->__class__==std::string("C"))) {
		auto _cast_c = std::static_pointer_cast<C>(c);
		std::cout << std::string("c is type C") << std::endl;
		std::cout << __shared__(_cast_c)->method() << std::endl;
		std::cout << __shared__(_cast_c)->bar() << std::endl;
	} else {
		std::cout << std::string("error: c is not type C") << std::endl;
	}
	if ((d->__class__==std::string("D"))) {
		auto _cast_d = std::static_pointer_cast<D>(d);
		std::cout << std::string("d is type D") << std::endl;
		std::cout << __shared__(_cast_d)->hey() << std::endl;
	} else {
		std::cout << std::string("error: d is not type D") << std::endl;
	}
	std::cout << std::string("------------------") << std::endl;
	for (int i=0; i<3; i++) {
		auto o = some_subclass(i);			/* new variable */
		std::cout << __shared__(o)->method() << std::endl;
		if ((o->__class__==std::string("B"))) {
			auto _cast_o = std::static_pointer_cast<B>(o);
			std::cout << __shared__(_cast_o)->foo() << std::endl;
		}
		if ((o->__class__==std::string("C"))) {
			auto _cast_o = std::static_pointer_cast<C>(o);
			std::cout << __shared__(_cast_o)->bar() << std::endl;
		}
	}
	std::cout << std::string("end of test") << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/free_memory.py](free_memory.py)
input:
------
```python
'''
delete pointer
'''
class A:
	def __init__(self, x:int ):
		self.x = x
	def __del__(self):
		print( 'goodbye')

def main():
	a = A(1)
	print a
	del a
	print 'done'
```
output:
------
```c++

class A {
  public:
	std::string __class__;
	int  x;
	A* __init__(int x);
	~A();
	A() {__class__ = std::string("A");}
	std::string getclassname() {return this->__class__;}
};
	A::~A() {

		std::cout << std::string("goodbye") << std::endl;
	}
	A* A::__init__(int x) {

		this->x = x;
		return this;
	}
int main() {

	auto a = std::shared_ptr<A>((new A())->__init__(1)); // new style
	std::cout << a << std::endl;
	a.reset();
	std::cout << std::string("done") << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/array_of_arrays_objects.py](array_of_arrays_objects.py)
input:
------
```python
'''
array of arrays objects
'''

class A:
	def __init__(self, id:int):
		self.id = id

	def method(self):
		print(self.id)

def main():
	a1 = A(1)
	a2 = A(2)
	a3 = A(3)

	arr = [][]A(
		(a1,a2,a3, A(4)),
		(a1,None),
		None,
	)
	print('length of array: ', len(arr))
	print( 'len subarray 0:  ', len(arr[0]) )
	print( 'len subarray 1:  ', len(arr[1]) )
	print('subarray 2 is nullptr:  ',arr[2] )
	print('subarray 0 ptr addr: ', arr[0])

	arr[0][2].method()
```
output:
------
```c++

class A {
  public:
	std::string __class__;
	int  id;
	A* __init__(int id);
	void method();
	A() {__class__ = std::string("A");}
	std::string getclassname() {return this->__class__;}
};
	void A::method() {

		std::cout << this->id << std::endl;
	}
	A* A::__init__(int id) {

		this->id = id;
		return this;
	}
int main() {

	auto a1 = std::shared_ptr<A>((new A())->__init__(1)); // new style
	auto a2 = std::shared_ptr<A>((new A())->__init__(2)); // new style
	auto a3 = std::shared_ptr<A>((new A())->__init__(3)); // new style
	/* arr = vector of vectors to: A */	
std::vector<  std::shared_ptr<A>  > _r__sub0_arr = {a1,a2,a3,std::shared_ptr<A>((new A())->__init__(4))};	
std::shared_ptr<std::vector<  std::shared_ptr<A>  >> _sub0_arr = std::make_shared<std::vector<  std::shared_ptr<A>  >>(_r__sub0_arr);	
std::vector<  std::shared_ptr<A>  > _r__sub1_arr = {a1,nullptr};	
std::shared_ptr<std::vector<  std::shared_ptr<A>  >> _sub1_arr = std::make_shared<std::vector<  std::shared_ptr<A>  >>(_r__sub1_arr);	
std::vector< std::shared_ptr<std::vector<  std::shared_ptr<A>  >> > _ref_arr = {_sub0_arr,_sub1_arr,nullptr};	
std::shared_ptr<std::vector< std::shared_ptr<std::vector<  std::shared_ptr<A>  >> >> arr = std::make_shared<std::vector< std::shared_ptr<std::vector<  std::shared_ptr<A>  >> >>(_ref_arr);
	std::cout << std::string("length of array: ");
std::cout << arr->size();std::cout << std::endl;
	std::cout << std::string("len subarray 0:  ");
std::cout << (*arr)[0]->size();std::cout << std::endl;
	std::cout << std::string("len subarray 1:  ");
std::cout << (*arr)[1]->size();std::cout << std::endl;
	std::cout << std::string("subarray 2 is nullptr:  ");
std::cout << (*arr)[2];std::cout << std::endl;
	std::cout << std::string("subarray 0 ptr addr: ");
std::cout << (*arr)[0];std::cout << std::endl;
	__shared__((*(*arr)[0])[2])->method();
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/cyclic_simple.py](cyclic_simple.py)
input:
------
```python
'''
detect cyclic parent/child, and insert weakref
'''
class Parent:
	def __init__(self, children:[]Child ):
		self.children = children

class Child:
	def __init__(self, parent:Parent ):
		self.parent = parent

	def foo(self) ->int:
		par = self.parent
		if par is not None:
			return 1
		else:
			print('parent is gone..')

	def bar(self):
		print self.parent.children

def make_child(p:Parent) -> Child:
	c = Child(p)
	p.children.push_back(c)
	return c


def main():
	children = []Child()
	p = Parent( children )
	c1 = make_child(p)
	c2 = make_child(p)
	print c1.foo()
	c1.bar()
	del p
	print c1.foo()
	#uncomment to segfault##c1.bar()
```
output:
------
```c++

class Parent {
  public:
	std::string __class__;
	std::shared_ptr<std::vector<std::shared_ptr<Child>>>  children;
	Parent* __init__(std::shared_ptr<std::vector<std::shared_ptr<Child>>> children);
	Parent() {__class__ = std::string("Parent");}
	std::string getclassname() {return this->__class__;}
};
class Child {
  public:
	std::string __class__;
	std::weak_ptr<Parent>  parent;
	Child* __init__(std::shared_ptr<Parent> parent);
	int foo();
	void bar();
	Child() {__class__ = std::string("Child");}
	std::string getclassname() {return this->__class__;}
};
std::shared_ptr<Child> make_child(std::shared_ptr<Parent> p) {

	auto c = std::shared_ptr<Child>((new Child())->__init__(p)); // new style
	__shared__(__shared__(p)->children)->push_back(c);
	return c;
}
	void Child::bar() {

		std::cout << __shared__(this->parent.lock())->children << std::endl;
	}
	int Child::foo() {

		auto par = this->parent.lock();  /* fallback */
		if (( par != nullptr )) {
			return 1;
		} else {
			std::cout << std::string("parent is gone..") << std::endl;
		}
	}
	Child* Child::__init__(std::shared_ptr<Parent> parent) {

		this->parent = parent;
		return this;
	}
	Parent* Parent::__init__(std::shared_ptr<std::vector<std::shared_ptr<Child>>> children) {

		this->children = children;
		return this;
	}
int main() {

	std::shared_ptr<std::vector<std::shared_ptr<Child>>> children( ( new std::vector<std::shared_ptr<Child>>({}) ) ); /* 1D Array */
	auto p = std::shared_ptr<Parent>((new Parent())->__init__(children)); // new style
	auto c1 = make_child(p);			/* new variable */
	auto c2 = make_child(p);			/* new variable */
	std::cout << __shared__(c1)->foo() << std::endl;
	__shared__(c1)->bar();
	p.reset();
	std::cout << __shared__(c1)->foo() << std::endl;
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/returns_array2D.py](returns_array2D.py)
input:
------
```python
'''
returns array of arrays
'''
def make_array() -> [][]int:
	arr = [][]int(
		(1,2,3),
		(4,5,6,7,8)
	)
	return arr

def test_array( arr:[][]int ):
	print( arr[0][0] )

def main():
	a = make_array()
	print( len(a))
	print( len(a[0]) )
	print( len(a[1]) )

	test_array(a)
```
output:
------
```c++

std::shared_ptr<std::vector<std::shared_ptr<std::vector<int>>>> make_array() {

	/* arr = vector of vectors to: int */	
std::vector<int> _r__sub0_arr = {1,2,3};	
std::shared_ptr<std::vector<int>> _sub0_arr = std::make_shared<std::vector<int>>(_r__sub0_arr);	
std::vector<int> _r__sub1_arr = {4,5,6,7,8};	
std::shared_ptr<std::vector<int>> _sub1_arr = std::make_shared<std::vector<int>>(_r__sub1_arr);	
std::vector< std::shared_ptr<std::vector<int>> > _ref_arr = {_sub0_arr,_sub1_arr};	
std::shared_ptr<std::vector< std::shared_ptr<std::vector<int>> >> arr = std::make_shared<std::vector< std::shared_ptr<std::vector<int>> >>(_ref_arr);
	return arr;
}
void test_array(std::shared_ptr<std::vector<std::shared_ptr<std::vector<int>>>> arr) {

	std::cout << (*(*arr)[0])[0] << std::endl;
}
int main() {

	auto a = make_array();			/* new variable */
	std::cout << a->size() << std::endl;
	std::cout << (*a)[0]->size() << std::endl;
	std::cout << (*a)[1]->size() << std::endl;
	test_array(a);
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/try_except_finally.py](try_except_finally.py)
input:
------
```python
'''
c++ finally
'''

def myfunc():

	a = False
	try:
		raise RuntimeError('oops')
	except RuntimeError:
		print 'caught RuntimeError OK'
		a = True

	assert a == True


	c = False
	try:
		raise IOError('my ioerror')

	except IOError as err:
		print 'caught my ioerr'
		print err.what()
		#raise err  ## rethrow works ok
		c = True
	assert c == True


	b = False

	try:
		print('trying something that will fail...')
		print('some call that fails at runtime')
		f = open('/tmp/nosuchfile')
	except RuntimeError:
		print 'this should not happen'
	except IOError:
		print 'CAUGHT IOError OK'
		## it is ok to raise or return in the except block,
		## the finally block will be run before any of this happens
		#raise RuntimeError('rethrowing error')  ## this works
		return

	except:
		print('CAUGHT UNKNOWN EXECEPTION')
		## raise another exception
		raise RuntimeError('got unknown exception')
	finally:
		print('FINALLY')
		b = True

	assert b == True





def main():
	myfunc()
```
output:
------
```c++

void myfunc() {

	auto a = false;  /* fallback */
	try {
		throw RuntimeError(std::string("oops"));
	}
	catch (std::runtime_error* __error__) {
		std::string __errorname__ = __parse_error_type__(__error__);
		if (__errorname__ == std::string("RuntimeError")) {
			std::cout << std::string("caught RuntimeError OK") << std::endl;
			a = true;
		}
	}
	if (!(( a == true ))) {throw std::runtime_error("assertion failed: ( a == true )"); }
	auto c = false;  /* fallback */
	try {
		throw IOError(std::string("my ioerror"));
	}
	catch (std::runtime_error* __error__) {
		std::string __errorname__ = __parse_error_type__(__error__);
		if (__errorname__ == std::string("IOError")) {
			auto err = *__error__;
			std::cout << std::string("caught my ioerr") << std::endl;
			std::cout << __shared__(err)->what() << std::endl;
			c = true;
		}
	}
	if (!(( c == true ))) {throw std::runtime_error("assertion failed: ( c == true )"); }
	auto b = false;  /* fallback */
	bool __finally_done_1 = false;
	try {
		std::cout << std::string("trying something that will fail...") << std::endl;
		std::cout << std::string("some call that fails at runtime") << std::endl;
		auto f = __open__(std::string("/tmp/nosuchfile"), std::string("rb"));			/* new variable */
	}
	catch (std::runtime_error* __error__) {
		std::string __errorname__ = __parse_error_type__(__error__);
		if (__errorname__ == std::string("RuntimeError")) {
			__finally_done_1 = true;
				try {		// finally block
					std::cout << std::string("FINALLY") << std::endl;
					b = true;
				} catch (...) {}
			std::cout << std::string("this should not happen") << std::endl;
		}
		if (__errorname__ == std::string("IOError")) {
			__finally_done_1 = true;
				try {		// finally block
					std::cout << std::string("FINALLY") << std::endl;
					b = true;
				} catch (...) {}
			std::cout << std::string("CAUGHT IOError OK") << std::endl;
			return;
		}
		if (__errorname__ == std::string("Error")) {
			__finally_done_1 = true;
				try {		// finally block
					std::cout << std::string("FINALLY") << std::endl;
					b = true;
				} catch (...) {}
			std::cout << std::string("CAUGHT UNKNOWN EXECEPTION") << std::endl;
			throw RuntimeError(std::string("got unknown exception"));
		}
	}
	if (__finally_done_1 == false) {
		try {		// finally block
			std::cout << std::string("FINALLY") << std::endl;
			b = true;
		} catch (...) {}
	}
	if (!(( b == true ))) {throw std::runtime_error("assertion failed: ( b == true )"); }
}
int main() {

	myfunc();
	return 0;
}
```
* [https://github.com/rusthon/Rusthon/tree/master/regtests/c++/if_else.py](if_else.py)
input:
------
```python
'''
simple if/else
'''


def main():
	a = 'x'
	if a == 'x':
		print('ok')
```
output:
------
```c++

int main() {

	auto a = std::string("x");  /* fallback */
	if (( a == std::string("x") )) {
		std::cout << std::string("ok") << std::endl;
	}
	return 0;
}
```