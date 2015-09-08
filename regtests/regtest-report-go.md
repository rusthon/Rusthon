Go Backend Regression Tests
-----------------------------
the following tests compiled, and the binary executed without any errors
* [array_of_objects.py](go/array_of_objects.py)

input:
------
```python
'''array of objects'''
class A:
    def foo(self) -> string:
        return 'xxxx'
class B(A):
    def foo(self) -> string:
        return 'hello'
class C(A):
    def foo(self) -> string:
        return 'world'


def push( arr:[]int, x:int ):
    arr.append( x )

#def push2( arr:[]*A, x:*A ):
#    arr.append( x )

def my_generic( s:A ):
    print( s.foo() )


def main():
    arr = []int()
    arr.append(1)
    push( arr, 100)
    assert len(arr)==2
    print(arr)

    a1 = A(); a2 = A(); a3 = A()
    obarr = []A( a1, a2 )
    print(obarr)

    print a3
    #push2( obarr, a3 )
    #print(obarr)
    #TestError( len(obarr)==3 )

    b1 = B()
    print(b1)
    #obarr.append( b1 )  ## fails because subclasses can not be cast to their base class

    #################################################
    barr = []B( b1, )  ## todo single item array should not require `,`
    c1 = C()
    barr.append( c1 )
    print(barr)

    bb = barr[0]
    print('bb:', bb)
    print(bb.foo())

    cc = barr[1]
    print('cc:', cc)
    print(cc.foo())

    #ccc = go.type_assert( cc, C )
    #print(ccc.foo())

    print('----testing generic----')
    for subclass in barr:
        print('subclass in bar:', subclass)
        my_generic(subclass)
```
output:
------
```go

type A struct {
__object__
}
func (self *A)  foo() string {

	return "xxxx"
}
func __new__A() *A {
  ob := A{}
  ob.__class__ = "A"
  return &ob
}
func (self *B)  A_foo() string {

	return "xxxx"
}
type B struct {
A
}
func (self *B)  foo() string {

	return "hello"
}
func __new__B() *B {
  ob := B{}
  ob.__class__ = "B"
  return &ob
}
func (self *C)  A_foo() string {

	return "xxxx"
}
type C struct {
A
}
func (self *C)  foo() string {

	return "world"
}
func __new__C() *C {
  ob := C{}
  ob.__class__ = "C"
  return &ob
}
func push(arr *[]int, x int) {

	__6 := append(*arr,x); *arr = __6;
}
func my_generic(__gen__ interface{}) {

	__type__ := "INVALID"
	__super__, __ok__ := __gen__.(object)
	if __ok__ { __type__ = __super__.getclassname();
	} else { fmt.Println("Gython RuntimeError - struct must implement the `object` interface"); }
	switch __type__ {
		case "C":
			s,__ok__ := __gen__.(*C)
			if __ok__ {
			fmt.Println(s.foo());
			} else {
				switch __gen__.(type) {
					case *B:
						s := C( *__gen__.(*B) )
						fmt.Println(s.foo());
					case *A:
 fmt.Println("Generics RuntimeError - can not cast base class to a subclass type", s);
				}
			}
		case "B":
			s,__ok__ := __gen__.(*B)
			if __ok__ {
			fmt.Println(s.foo());
			} else {
				switch __gen__.(type) {
					case *C:
						s := B( *__gen__.(*C) )
						fmt.Println(s.foo());
					case *A:
 fmt.Println("Generics RuntimeError - can not cast base class to a subclass type", s);
				}
			}
		case "A":
			s,__ok__ := __gen__.(*A)
			if __ok__ {
			fmt.Println(s.foo());
			} else {
 fmt.Println("Generics RuntimeError - generic argument is not a pointer to a struct", s);
 fmt.Println("struct: ",__gen__);
			}
	}
}
func main() {

	arr := &[]int{};
	__7 := append(*arr,1); *arr = __7;
	push(arr, 100)
	if ((( len(*arr) ) == 2) == false) { panic("assertion failed"); }
	fmt.Println(arr);
	a1 := __new__A();
	a2 := __new__A();
	a3 := __new__A();
	obarr := &[]*A{a1, a2};
	fmt.Println(obarr);
	fmt.Println(a3);
	b1 := __new__B();
	fmt.Println(b1);
	barr := &[]*B{b1};
	c1 := __new__C();
	__addr8 := B(*c1);__8 := append(*barr,&__addr8); *barr = __8;
	fmt.Println(barr);
	__subclass__ := (*barr)[0]
	switch __subclass__.__class__ {
		case "C":
			__addr := C(*__subclass__)
			bb := &__addr
			fmt.Println("bb:", bb);
			fmt.Println(bb.foo());
			__subclass__ := (*barr)[1]
			switch __subclass__.__class__ {
				case "C":
					__addr := C(*__subclass__)
					cc := &__addr
					fmt.Println("cc:", cc);
					fmt.Println(cc.foo());
					fmt.Println("----testing generic----");
					for _,subclass := range *barr {
						fmt.Println("subclass in bar:", subclass);
						my_generic(subclass)
					}
				case "B":
					__addr := B(*__subclass__)
					cc := &__addr
					fmt.Println("cc:", cc);
					fmt.Println(cc.foo());
					fmt.Println("----testing generic----");
					for _,subclass := range *barr {
						fmt.Println("subclass in bar:", subclass);
						my_generic(subclass)
					}
			}
		case "B":
			__addr := B(*__subclass__)
			bb := &__addr
			fmt.Println("bb:", bb);
			fmt.Println(bb.foo());
			__subclass__ := (*barr)[1]
			switch __subclass__.__class__ {
				case "C":
					__addr := C(*__subclass__)
					cc := &__addr
					fmt.Println("cc:", cc);
					fmt.Println(cc.foo());
					fmt.Println("----testing generic----");
					for _,subclass := range *barr {
						fmt.Println("subclass in bar:", subclass);
						my_generic(subclass)
					}
				case "B":
					__addr := B(*__subclass__)
					cc := &__addr
					fmt.Println("cc:", cc);
					fmt.Println(cc.foo());
					fmt.Println("----testing generic----");
					for _,subclass := range *barr {
						fmt.Println("subclass in bar:", subclass);
						my_generic(subclass)
					}
			}
	}
}
type _kwargs_type_ struct {
}
```
* [print.py](go/print.py)

input:
------
```python
"""hello world"""

XXX = 'myglobal'  ## this is a static string

def myprint( a:string, b:string ):
	print a + b


def main():
	print "hi"
	myprint('hello ', 'world')

	## TODO - should this automatically be converted from a static string to a String with `String.from_str()`
	myprint('hi ', str(XXX) )
```
output:
------
```go

var XXX = "myglobal";
func myprint(a string, b string) {

	fmt.Println((a + b));
}
func main() {

	fmt.Println("hi");
	myprint("hello ", "world")
	myprint("hi ", str(XXX))
}
type _kwargs_type_ struct {
}
```
* [func_calls.py](go/func_calls.py)

input:
------
```python
"""function call"""
def f(a:int, b:int, c:int) ->int:
	print 'testing f: plain args'
	return a+b+c

def f2(a:int=1, b:int=2, c:int=3) ->int:
	print 'testing f2: keyword args'
	return a+b+c

def f3( *args:int ) ->int:
	print 'testing f3: star args'
	return args[0] + args[1] + args[2]


def main():
	assert f(1,2,3) == 6

	x = f2( b=100 )
	assert x==104

	arr = [1,2,3]
	y = f3( *arr )
	assert y==6
```
output:
------
```go

func f(a int, b int, c int) int {

	fmt.Println("testing f: plain args");
	return ((a + b) + c)
}
func f2(__kwargs _kwargs_type_) int {

	a := 1
	if __kwargs.__use__a { a = __kwargs.a }
	b := 2
	if __kwargs.__use__b { b = __kwargs.b }
	c := 3
	if __kwargs.__use__c { c = __kwargs.c }
	fmt.Println("testing f2: keyword args");
	return ((a + b) + c)
}
func f3(__vargs__ ...int) int {

	args := &__vargs__
	fmt.Println("testing f3: star args");
	return (((*args)[0] + (*args)[1]) + (*args)[2])
}
func main() {

	if ((( f(1, 2, 3) ) == 6) == false) { panic("assertion failed"); }
	x := f2(_kwargs_type_{b:100,__use__b:true});
	if ((( x ) == 104) == false) { panic("assertion failed"); }
	arr := &[]int{1, 2, 3};
	y := f3(*arr...);
	if ((( y ) == 6) == false) { panic("assertion failed"); }
}
type _kwargs_type_ struct {
  a int
  __use__a bool
  c int
  __use__c bool
  b int
  __use__b bool
}
```
* [nested_func.py](go/nested_func.py)

input:
------
```python
'''
lambda func
'''

def main():
	def F(x:int) ->int:
		return x*2

	a = F(10)
	print a
	assert a==20
```
output:
------
```go

func main() {

	F := func (x int) int {

		return (x * 2)
	}
	a := F(10);
	fmt.Println(a);
	if ((( a ) == 20) == false) { panic("assertion failed"); }
}
type _kwargs_type_ struct {
}
```
* [arrays.py](go/arrays.py)

input:
------
```python
"""array types"""

def test_pass_array_as_arg( arr:[]int ):
	arr.append( 5 )

def main():
	a = []int(1,2,3)
	print a
	assert a[0]==1
	assert len(a)==3
	a.append( 4 )
	assert len(a)==4

	test_pass_array_as_arg( a )
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
```go

func test_pass_array_as_arg(arr *[]int) {

	__4 := append(*arr,5); *arr = __4;
}
func main() {

	a := &[]int{1, 2, 3};
	fmt.Println(a);
	if ((( (*a)[0] ) == 1) == false) { panic("assertion failed"); }
	if ((( len(*a) ) == 3) == false) { panic("assertion failed"); }
	__5 := append(*a,4); *a = __5;
	if ((( len(*a) ) == 4) == false) { panic("assertion failed"); }
	test_pass_array_as_arg(a)
	if ((( len(*a) ) == 5) == false) { panic("assertion failed"); }
	b := &[2]int{100, 200};
	if ((( (*b)[0] ) == 100) == false) { panic("assertion failed"); }
	if ((( (*b)[1] ) == 200) == false) { panic("assertion failed"); }
}
type _kwargs_type_ struct {
}
```
* [vars.py](go/vars.py)

input:
------
```python
"""var assignment :=, and reassignment ="""

def main():
	a = 1
	print a
	a = 2
	print a
	assert a==2
```
output:
------
```go

func main() {

	a := 1;
	fmt.Println(a);
	a = 2;
	fmt.Println(a);
	if ((( a ) == 2) == false) { panic("assertion failed"); }
}
type _kwargs_type_ struct {
}
```
* [chan.py](go/chan.py)

input:
------
```python
"""send int over channel"""

def wrapper(a:int, c: chan int):
	result = 100
	c <- result

def main():
	c = channel(int)

	spawn( wrapper(17, c) )

	# Do other work in the current goroutine until the channel has a result.

	x = <-c
	print(x)
	assert x==100
```
output:
------
```go

func wrapper(a int, c chan int) {

	result := 100;
	c <- result;
}
func main() {

	c := make(chan int);
	go wrapper(17, c)
	x := <- c;
	fmt.Println(x);
	if ((( x ) == 100) == false) { panic("assertion failed"); }
}
type _kwargs_type_ struct {
}
```
* [loop_map.py](go/loop_map.py)

input:
------
```python
'''
map loop
'''

def main():
	a = {'x':100, 'y':200}
	b = ''
	c = 0
	for key, value in a:
		print( key )
		print( value )
		b += key
		c += value

	print( b )
	print( c )
```
output:
------
```go

func main() {

	a := &map[string]int{ "x":100, "y":200 };
	b := "";
	c := 0;
	for key,value := range *a {
		fmt.Println(key);
		fmt.Println(value);
		b += key;
		c += value;
	}
	fmt.Println(b);
	fmt.Println(c);
}
type _kwargs_type_ struct {
}
```
* [generics_subclasses.py](go/generics_subclasses.py)

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

class B(A):

	def method1(self) ->int:
		return self.x * 2

class C(A):

	def method1(self) ->int:
		return self.x + 200


def my_generic( g:A ) ->int:
	return g.method1()

def main():
	a = A( 100 )
	b = B( 100 )
	c = C( 100 )
	print a
	print b
	print c

	x = my_generic( a )
	assert a.x == x

	y = my_generic( b )
	assert y==200

	z = my_generic( c )
	assert z==300
```
output:
------
```go

type A struct {
__object__
x int
}
func (self *A)  __init__(x int) *A {

	self.x = x;
return self
}
func (self *A)  method1() int {

	return self.x
}
func __new__A( x int ) *A {
  ob := A{}
  ob.__init__(x)
  ob.__class__ = "A"
  return &ob
}
func (self *B)  __init__(x int) *B {

	self.x = x;
return self
}
func (self *B)  A_method1() int {

	return self.x
}
type B struct {
A
}
func (self *B)  method1() int {

	return (self.x * 2)
}
func __new__B( x int ) *B {
  ob := B{}
  ob.__init__(x)
  ob.__class__ = "B"
  return &ob
}
func (self *C)  __init__(x int) *C {

	self.x = x;
return self
}
func (self *C)  A_method1() int {

	return self.x
}
type C struct {
A
}
func (self *C)  method1() int {

	return (self.x + 200)
}
func __new__C( x int ) *C {
  ob := C{}
  ob.__init__(x)
  ob.__class__ = "C"
  return &ob
}
func my_generic(__gen__ interface{}) int {

	__type__ := "INVALID"
	__super__, __ok__ := __gen__.(object)
	if __ok__ { __type__ = __super__.getclassname();
	} else { fmt.Println("Gython RuntimeError - struct must implement the `object` interface"); }
	switch __type__ {
		case "C":
			g,__ok__ := __gen__.(*C)
			if __ok__ {
			return g.method1()
			} else {
				switch __gen__.(type) {
					case *B:
						g := C( *__gen__.(*B) )
						return g.method1()
					case *A:
 fmt.Println("Generics RuntimeError - can not cast base class to a subclass type", g);
				}
			}
		case "B":
			g,__ok__ := __gen__.(*B)
			if __ok__ {
			return g.method1()
			} else {
				switch __gen__.(type) {
					case *C:
						g := B( *__gen__.(*C) )
						return g.method1()
					case *A:
 fmt.Println("Generics RuntimeError - can not cast base class to a subclass type", g);
				}
			}
		case "A":
			g,__ok__ := __gen__.(*A)
			if __ok__ {
			return g.method1()
			} else {
 fmt.Println("Generics RuntimeError - generic argument is not a pointer to a struct", g);
 fmt.Println("struct: ",__gen__);
			}
	}
	fmt.Println("Generics RuntimeError - failed to convert type to:", __type__, __gen__)
	return 0
}
func main() {

	a := __new__A(100);
	b := __new__B(100);
	c := __new__C(100);
	fmt.Println(a);
	fmt.Println(b);
	fmt.Println(c);
	x := my_generic(a);
	if ((( a.x ) == x) == false) { panic("assertion failed"); }
	y := my_generic(b);
	if ((( y ) == 200) == false) { panic("assertion failed"); }
	z := my_generic(c);
	if ((( z ) == 300) == false) { panic("assertion failed"); }
}
type _kwargs_type_ struct {
}
```
* [list_comprehension.py](go/list_comprehension.py)

input:
------
```python
'''
go list comprehensions
'''

class A:
	def __init__(self, x:int,arr:[]int):
		## note: names of args should match names on struct
		self.x = x
		self.arr = arr
		## TODO FIXME: allow arg names to be different from internal struct names
		#let self.arr : []int  = y

	def get(self) ->int:
		return self.arr[3] + self.x


def F( arr:[]int ):
	arr.append( 3 )

def main():
	a = []int(x for x in range(3))
	print a
	F( a )
	assert len(a)==4
	assert a[0]==0
	assert a[1]==1
	assert a[2]==2
	assert a[3]==3

	b = []A( 
		A(i,a) for i in range(2) 
	)
	assert b[1].get()==4
	print b
```
output:
------
```go

type A struct {
__object__
x int
arr *[]int
}
func (self *A)  __init__(x int, arr *[]int) *A {

	self.x = x;
	self.arr = arr;
return self
}
func (self *A)  get() int {

	return ((*self.arr)[3] + self.x)
}
func __new__A( x int,arr *[]int ) *A {
  ob := A{}
  ob.__init__(x,arr)
  ob.__class__ = "A"
  return &ob
}
func F(arr *[]int) {

	__2 := append(*arr,3); *arr = __2;
}
func main() {

	__comp__0 := []int{};
	idx0 := 0;
	iter0 := 3;
	for ( idx0 ) < iter0 {
		
		x := idx0;
		__comp__0 = append(__comp__0, x);
		idx0 ++;
	}
	a := &__comp__0;
	fmt.Println(a);
	F(a)
	if ((( len(*a) ) == 4) == false) { panic("assertion failed"); }
	if ((( (*a)[0] ) == 0) == false) { panic("assertion failed"); }
	if ((( (*a)[1] ) == 1) == false) { panic("assertion failed"); }
	if ((( (*a)[2] ) == 2) == false) { panic("assertion failed"); }
	if ((( (*a)[3] ) == 3) == false) { panic("assertion failed"); }
	__comp__1 := []*A{};
	idx1 := 0;
	iter1 := 2;
	for ( idx1 ) < iter1 {
		
		i := idx1;
		__comp__1 = append(__comp__1, __new__A(i, a));
		idx1 ++;
	}
	b := &__comp__1;
	if ((( (*b)[1].get() ) == 4) == false) { panic("assertion failed"); }
	fmt.Println(b);
}
type _kwargs_type_ struct {
}
```
* [class.py](go/class.py)

input:
------
```python
'''
simple class
'''
class A:
	{
		x:int,
		y:int,
		z:int,
	}
	def __init__(self, x:int, y:int, z:int=1):
		self.x = x
		self.y = y
		self.z = z

	def mymethod(self, m:int) -> int:
		return self.x * m

def call_method( cb:func(int)(int), mx:int ) ->int:
	return cb(mx)

def main():
	a = A( 100, 200, z=9999 )
	print( a.x )
	print( a.y )
	print( a.z )

	b = a.mymethod(3)
	print( b )

	c = call_method( a.mymethod, 4 )
	print( c )
```
output:
------
```go

type A struct {
__object__
y int
x int
z int
}
func (self *A)  __init__(x int, y int, __kwargs _kwargs_type_) *A {

	z := 1
	if __kwargs.__use__z { z = __kwargs.z }
	self.x = x;
	self.y = y;
	self.z = z;
return self
}
func (self *A)  mymethod(m int) int {

	return (self.x * m)
}
func __new__A( x int,y int,__kwargs _kwargs_type_ ) *A {
  ob := A{}
  ob.__init__(x,y,__kwargs)
  ob.__class__ = "A"
  return &ob
}
func call_method(cb func(int)(int), mx int) int {

	return cb(mx)
}
func main() {

	a := __new__A(100, 200,_kwargs_type_{z:9999,__use__z:true});
	fmt.Println(a.x);
	fmt.Println(a.y);
	fmt.Println(a.z);
	b := a.mymethod(3);
	fmt.Println(b);
	c := call_method(a.mymethod, 4);
	fmt.Println(c);
}
type _kwargs_type_ struct {
  z int
  __use__z bool
}
```
* [go_select.py](go/go_select.py)

input:
------
```python
"""go select"""

def send_data( A:chan int, B:chan int, X:int, Y:int):
	while True:
		print('sending data..')
		A <- X
		B <- Y

def select_loop(A:chan int, B:chan int, W:chan int) -> int:
	print('starting select loop')
	y = 0
	while True:
		print('select loop:',y)
		select:
			case x = <- A:
				y += x
				W <- y
			case x = <- B:
				y += x
				W <- y
	print('end select loop', y)
	return y

def main():
	a = go.channel(int)
	b = go.channel(int)
	w = go.channel(int)

	go(
		select_loop(a,b, w)
	)


	go(
		send_data(a,b, 5, 10)
	)

	z = 0
	while z < 100:
		z = <- w
		print('main loop', z)

	print('end test')
```
output:
------
```go

func send_data(A chan int, B chan int, X int, Y int) {

	for  {
		fmt.Println("sending data..");
		A <- X;
		B <- Y;
	}
}
func select_loop(A chan int, B chan int, W chan int) int {

	fmt.Println("starting select loop");
	y := 0;
	for  {
		fmt.Println("select loop:", y);
				select {
				case x := <- A: {
		y += x;
		W <- y;
		 break;}
				case x := <- B: {
		y += x;
		W <- y;
		 break;}
		}
	}
	fmt.Println("end select loop", y);
	return y
}
func main() {

	a := make(chan int);
	b := make(chan int);
	w := make(chan int);
	go select_loop(a, b, w)
	go send_data(a, b, 5, 10)
	z := 0;
	for ( z ) < 100 {
		z = <- w;
		fmt.Println("main loop", z);
	}
	fmt.Println("end test");
}
type _kwargs_type_ struct {
}
```
* [generics_methods.py](go/generics_methods.py)

input:
------
```python
class G:
	def method(self):
		print 'calling G.method'
		print 'hi'

class H( G ):
	def method(self):
		print 'calling H.method'
		print 'world'

class A:
	def __init__(self, a:G):
		print 'A.__init__'
		print(a)
		self.x = a

	def call(self):
		print 'A.call'
		self.f( self.x )

	def f(self, a:G):
		print 'A.f'
		print(a)


class B( A ):
	def f(self, g:G):
		print 'B.f'
		g.method()



def main():
	g = G()
	h = H()
	b1 = B( g )
	b2 = B( h )

	print('----------test1 b1 (g)')
	b1.call()
	print('----------test2 b2 (h)')
	b2.call()
```
output:
------
```go

type G struct {
__object__
}
func (self *G)  method() {

	fmt.Println("calling G.method");
	fmt.Println("hi");
}
func __new__G() *G {
  ob := G{}
  ob.__class__ = "G"
  return &ob
}
func (self *H)  G_method() {

	fmt.Println("calling G.method");
	fmt.Println("hi");
}
type H struct {
G
}
func (self *H)  method() {

	fmt.Println("calling H.method");
	fmt.Println("world");
}
func __new__H() *H {
  ob := H{}
  ob.__class__ = "H"
  return &ob
}
type A struct {
__object__
a G
x interface{}
}
func (self *A)  __init__(a interface{}) *A {

	fmt.Println("A.__init__");
	fmt.Println(a);
	self.x = a;
return self
}
func (self *A)  call() {

	fmt.Println("A.call");
	self.f(self.x)
}
func (self *A)  f(__gen__ interface{}) {

	__type__ := "INVALID"
	__super__, __ok__ := __gen__.(object)
	if __ok__ { __type__ = __super__.getclassname();
	} else { fmt.Println("Gython RuntimeError - struct must implement the `object` interface"); }
	switch __type__ {
	}
}
func __new__A( a interface{} ) *A {
  ob := A{}
  ob.__init__(a)
  ob.__class__ = "A"
  return &ob
}
func (self *B)  __init__(a interface{}) *B {

	fmt.Println("A.__init__");
	fmt.Println(a);
	self.x = a;
return self
}
func (self *B)  call() {

	fmt.Println("A.call");
	self.f(self.x)
}
func (self *B)  A_f(__gen__ interface{}) {

	__type__ := "INVALID"
	__super__, __ok__ := __gen__.(object)
	if __ok__ { __type__ = __super__.getclassname();
	} else { fmt.Println("Gython RuntimeError - struct must implement the `object` interface"); }
	switch __type__ {
		case "H":
			a,__ok__ := __gen__.(*H)
			if __ok__ {
			fmt.Println("A.f");
			fmt.Println(a);
			} else {
				switch __gen__.(type) {
					case *G:
 fmt.Println("Generics RuntimeError - can not cast base class to a subclass type", a);
				}
			}
	}
}
type B struct {
A
}
func (self *B)  f(__gen__ interface{}) {

	__type__ := "INVALID"
	__super__, __ok__ := __gen__.(object)
	if __ok__ { __type__ = __super__.getclassname();
	} else { fmt.Println("Gython RuntimeError - struct must implement the `object` interface"); }
	switch __type__ {
		case "H":
			g,__ok__ := __gen__.(*H)
			if __ok__ {
			fmt.Println("B.f");
			g.method()
			} else {
				switch __gen__.(type) {
					case *G:
 fmt.Println("Generics RuntimeError - can not cast base class to a subclass type", g);
				}
			}
	}
}
func __new__B( a interface{} ) *B {
  ob := B{}
  ob.__init__(a)
  ob.__class__ = "B"
  return &ob
}
func main() {

	g := __new__G();
	h := __new__H();
	b1 := __new__B(g);
	b2 := __new__B(h);
	fmt.Println("----------test1 b1 (g)");
	b1.call()
	fmt.Println("----------test2 b2 (h)");
	b2.call()
}
type _kwargs_type_ struct {
}
```
* [subclass.py](go/subclass.py)

input:
------
```python
'''
simple class
'''
class A:
	def __init__(self, x:int, y:int, z:int=1):
		let self.x : int = x
		let self.y : int = y
		let self.z : int = z

	def mymethod(self, m:int) -> int:
		return self.x * m

class B(A):
	def __init__(self, s:string):
		let self.w : string = s
		let self.x : int = 1

	def method2(self, v:string) ->string:
		print(self.x)
		self.w = v
		return self.w

def call_method( cb:func(int)(int), mx:int ) ->int:
	return cb(mx)

def main():
	a = A( 100, 200, z=9999 )
	print( a.x )
	print( a.y )
	print( a.z )

	b = a.mymethod(3)
	print( b )

	c = call_method( a.mymethod, 4 )
	print( c )

	x = B('testing...')
	print( x.method2('hello world') )
```
output:
------
```go

type A struct {
__object__
y int
x int
z int
}
func (self *A)  __init__(x int, y int, __kwargs _kwargs_type_) *A {

	z := 1
	if __kwargs.__use__z { z = __kwargs.z }
	self.x = x
	self.y = y
	self.z = z
return self
}
func (self *A)  mymethod(m int) int {

	return (self.x * m)
}
func __new__A( x int,y int,__kwargs _kwargs_type_ ) *A {
  ob := A{}
  ob.__init__(x,y,__kwargs)
  ob.__class__ = "A"
  return &ob
}
func (self *B)  A___init__(x int, y int, __kwargs _kwargs_type_) *B {

	z := 1
	if __kwargs.__use__z { z = __kwargs.z }
	self.x = x
	self.y = y
	self.z = z
return self
}
func (self *B)  mymethod(m int) int {

	return (self.x * m)
}
type B struct {
A
s string
w string
}
func (self *B)  __init__(s string) *B {

	self.w = s
	self.x = 1
return self
}
func (self *B)  method2(v string) string {

	fmt.Println(self.x);
	self.w = v;
	return self.w
}
func __new__B( s string ) *B {
  ob := B{}
  ob.__init__(s)
  ob.__class__ = "B"
  return &ob
}
func call_method(cb func(int)(int), mx int) int {

	return cb(mx)
}
func main() {

	a := __new__A(100, 200,_kwargs_type_{z:9999,__use__z:true});
	fmt.Println(a.x);
	fmt.Println(a.y);
	fmt.Println(a.z);
	b := a.mymethod(3);
	fmt.Println(b);
	c := call_method(a.mymethod, 4);
	fmt.Println(c);
	x := __new__B("testing...");
	fmt.Println(x.method2("hello world"));
}
type _kwargs_type_ struct {
  z int
  __use__z bool
}
```
* [maps.py](go/maps.py)

input:
------
```python
"""map types"""

def main():
	a = map[string]int{
		'x': 1,
		'y': 2,
		'z': 3,
	}

	print( a['x'] )
	assert a['x']==1

	b = map[int]string{ 0:'a', 1:'b' }
	print( b[0] )
	print( b[1] )
	assert b[0]=='a'
	assert b[1]=='b'

	## infers type of key and value ##
	c = {'x':100, 'y':200}
	print( c['x'] )
	print( c['y'] )

	assert c['x']==100
	assert c['y']==200 
```
output:
------
```go

func main() {

	a := &map[string]int{ "x":1, "y":2, "z":3 };
	fmt.Println((*a)["x"]);
	if ((( (*a)["x"] ) == 1) == false) { panic("assertion failed"); }
	b := &map[int]string{ 0:"a", 1:"b" };
	fmt.Println((*b)[0]);
	fmt.Println((*b)[1]);
	if ((( (*b)[0] ) == "a") == false) { panic("assertion failed"); }
	if ((( (*b)[1] ) == "b") == false) { panic("assertion failed"); }
	c := &map[string]int{ "x":100, "y":200 };
	fmt.Println((*c)["x"]);
	fmt.Println((*c)["y"]);
	if ((( (*c)["x"] ) == 100) == false) { panic("assertion failed"); }
	if ((( (*c)["y"] ) == 200) == false) { panic("assertion failed"); }
}
type _kwargs_type_ struct {
}
```
* [loop_arrays.py](go/loop_arrays.py)

input:
------
```python
'''
array loop
'''

def main():

	a = [1,2,3]
	y = 0
	for x in a:
		y += x
	assert y==6

	z = ''
	arr = ['a', 'b', 'c']
	for v in arr:
		z += v
	assert z == 'abc'

	b = 0
	for i in range(10):
		b += 1
	assert b == 10

	b2 = 0
	for i in range(5, 10):
		b2 += 1
	assert b2 == 5


	c = ''
	d = 0
	for i,v in enumerate(arr):
		c += v
		d += i
	assert c == 'abc'

	e = 0
	for i in range( len(arr) ):
		e += 1
	assert e == 3

	s = a[:2]
	print('len of s:')
	print(len(s))
	assert len(s)==2

	s2 = a[2:]
	print('len of s2:')
	print(len(s2))
	print(s2[0])
	assert len(s2)==1

	#e = 0
	#for i in s:
	#	e += i
	#TestError( e == 3 )
		
```
output:
------
```go

func main() {

	a := &[]int{1, 2, 3};
	y := 0;
	for _,x := range *a {
		y += x;
	}
	if ((( y ) == 6) == false) { panic("assertion failed"); }
	z := "";
	arr := &[]string{"a", "b", "c"};
	for _,v := range *arr {
		z += v;
	}
	if ((( z ) == "abc") == false) { panic("assertion failed"); }
	b := 0;
	for i := 0; i < 10; i++ {
		b ++;
	}
	if ((( b ) == 10) == false) { panic("assertion failed"); }
	b2 := 0;
	for i := 5; i < 10; i++ {
		b2 ++;
	}
	if ((( b2 ) == 5) == false) { panic("assertion failed"); }
	c := "";
	d := 0;
	for i,v := range *arr {
		c += v;
		d += i;
	}
	if ((( c ) == "abc") == false) { panic("assertion failed"); }
	e := 0;
	for i := 0; i < len(*arr); i++ {
		e ++;
	}
	if ((( e ) == 3) == false) { panic("assertion failed"); }
	__slice5 := (*a)[:2]; s := &__slice5;
	fmt.Println("len of s:");
	fmt.Println(len(*s));
	if ((( len(*s) ) == 2) == false) { panic("assertion failed"); }
	__slice6 := (*a)[2:]; s2 := &__slice6;
	fmt.Println("len of s2:");
	fmt.Println(len(*s2));
	fmt.Println((*s2)[0]);
	if ((( len(*s2) ) == 1) == false) { panic("assertion failed"); }
}
type _kwargs_type_ struct {
}
```
* [map_comprehension.py](go/map_comprehension.py)

input:
------
```python
'''
map comprehensions
'''

def main():
	m = map[int]string{ 
		key:'xxx' for key in range(10)
	}
	assert m[0]=='xxx'
	assert m[9]=='xxx'
	print m
	print m[0]
	print m[1]
```
output:
------
```go

func main() {

	__comp__0 := &map[int]string{  };
	idx0 := 0;
	iter0 := 10;
	for ( idx0 ) < iter0 {
		
		key := idx0;
		(*__comp__0)[key] = "xxx";
		idx0 ++;
	}
	m := __comp__0;
	if ((( (*m)[0] ) == "xxx") == false) { panic("assertion failed"); }
	if ((( (*m)[9] ) == "xxx") == false) { panic("assertion failed"); }
	fmt.Println(m);
	fmt.Println((*m)[0]);
	fmt.Println((*m)[1]);
}
type _kwargs_type_ struct {
}
```
* [callback_in_class.py](go/callback_in_class.py)

input:
------
```python
'''
callback in class
'''
class A:
	def __init__(self, cb:func(int)(int), x:int, y:int, z:int=1):
		let self.x : int = x
		let self.y : int = y
		let self.z : int = z
		let self.callback : func(int)(int) = cb

	def call(self, a:int ) -> int:
		return self.callback( a + self.x + self.y + self.z )

def mycb( x:int ) ->int:
	return x + 1000

def main():
	a = A(
		mycb, 
		100, 
		200, 
		z=300
	)
	#print( a.x )
	#print( a.y )
	#print( a.z )

	assert a.call(-600)==1000
	print 'ok'

```
output:
------
```go

type A struct {
__object__
y int
x int
z int
callback func(int)(int)
cb func(int)(int)
}
func (self *A)  __init__(cb func(int)(int), x int, y int, __kwargs _kwargs_type_) *A {

	z := 1
	if __kwargs.__use__z { z = __kwargs.z }
	self.x = x
	self.y = y
	self.z = z
	self.callback = cb
return self
}
func (self *A)  call(a int) int {

	return self.callback((((a + self.x) + self.y) + self.z))
}
func __new__A( cb func(int)(int),x int,y int,__kwargs _kwargs_type_ ) *A {
  ob := A{}
  ob.__init__(cb,x,y,__kwargs)
  ob.__class__ = "A"
  return &ob
}
func mycb(x int) int {

	return (x + 1000)
}
func main() {

	a := __new__A(mycb, 100, 200,_kwargs_type_{z:300,__use__z:true});
	if ((( a.call(-600) ) == 1000) == false) { panic("assertion failed"); }
	fmt.Println("ok");
}
type _kwargs_type_ struct {
  z int
  __use__z bool
}
```