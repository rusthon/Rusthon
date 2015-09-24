JavaScript Backend Regression Tests - class
-----------------------------
the following tests compiled, and run in nodejs without any errors
* [isinstance.py](class/isinstance.py)

input:
------
```python
from runtime import *
'''
builtin isinstance
'''
class A():
	pass

class B:
	pass

def main():
	print 'testing isinstance'
	a = A()
	b = B()
	assert( isinstance(a,A)==True )
	assert( isinstance(a,B)==False )
	assert( isinstance(a,dict)==False )

	assert( isinstance(b,B)==True )
	assert( isinstance(b,A)==False )

	c = [1,2]
	assert( isinstance(c, list)==True )
	assert( isinstance(c, dict)==False )
	assert( isinstance(c, A)==False )

	d = {'a':1, 'b':2}
	assert( isinstance(d, dict)==True )
	assert( isinstance(d, A)==False )

	print 'ok'

main()
```
output:
------
```javascript


var A =  function A()
{
/***/ if (A.__recompile !== undefined) { eval("A.__redef="+A.__recompile); A.__recompile=undefined; };
/***/ if (A.__redef !== undefined) { return A.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
/***/ if (A_toString.__recompile !== undefined) { eval("A_toString.__redef="+A_toString.__recompile); A_toString.__recompile=undefined; };
/***/ if (A_toString.__redef !== undefined) { return A_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

var B =  function B()
{
/***/ if (B.__recompile !== undefined) { eval("B.__redef="+B.__recompile); B.__recompile=undefined; };
/***/ if (B.__redef !== undefined) { return B.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`B`	*/

B.prototype.__class__ = B;
B.__name__ = "B";
B.__bases__ = [];
B.prototype.toString =  function B_toString()
{
/***/ if (B_toString.__recompile !== undefined) { eval("B_toString.__redef="+B_toString.__recompile); B_toString.__recompile=undefined; };
/***/ if (B_toString.__redef !== undefined) { return B_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b,d;
	console.log("testing isinstance");
	a =  new A();
	b =  new B();
	if (!(isinstance(a, A) === true)) {throw new Error("assertion failed"); }
	if (!(isinstance(a, B) === false)) {throw new Error("assertion failed"); }
	if (!(isinstance(a, dict) === false)) {throw new Error("assertion failed"); }
	if (!(isinstance(b, B) === true)) {throw new Error("assertion failed"); }
	if (!(isinstance(b, A) === false)) {throw new Error("assertion failed"); }
	c = [1, 2];
	if (!(isinstance(c, list) === true)) {throw new Error("assertion failed"); }
	if (!(isinstance(c, dict) === false)) {throw new Error("assertion failed"); }
	if (!(isinstance(c, A) === false)) {throw new Error("assertion failed"); }
	d = dict({  }, { copy:false, keytype:"string", iterable:[["a", 1], ["b", 2]] });
	if (!(isinstance(d, dict) === true)) {throw new Error("assertion failed"); }
	if (!(isinstance(d, A) === false)) {throw new Error("assertion failed"); }
	console.log("ok");
}/*end->	`main`	*/

main();
```
* [init_keyword.py](class/init_keyword.py)

input:
------
```python
from runtime import *
'''
test __init__ with keyword arg
'''

def main():
    class Cell:
        def __init__(self, x=1):
            self.x = x

    a = Cell(x=2)
    assert(a.x == 2)
main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a;
			var Cell =  function Cell(x)
	{
/***/ if (Cell.__recompile !== undefined) { eval("Cell.__redef="+Cell.__recompile); Cell.__recompile=undefined; };
/***/ if (Cell.__redef !== undefined) { return Cell.__redef.apply(this,arguments); };
		this.__$UID$__ = __$UID$__ ++;
		/***/ try {
		this.__init__(x);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, Cell, this.__init__)==true){debugger;}else{throw __err;} };
	}/*end->	`Cell`	*/

	Cell.prototype.__class__ = Cell;
	Cell.__name__ = "Cell";
	Cell.__bases__ = [];
			Cell.prototype.toString =  function Cell_toString()
	{
/***/ if (Cell_toString.__recompile !== undefined) { eval("Cell_toString.__redef="+Cell_toString.__recompile); Cell_toString.__recompile=undefined; };
/***/ if (Cell_toString.__redef !== undefined) { return Cell_toString.__redef.apply(this,arguments); };
		return this.__$UID$__;
	}/*end->	`toString`	*/

			Cell.prototype.__init__ =  function Cell___init__(_kwargs_)
	{
/***/ if (Cell___init__.__recompile !== undefined) { eval("Cell___init__.__redef="+Cell___init__.__recompile); Cell___init__.__recompile=undefined; };
/***/ if (Cell___init__.__redef !== undefined) { return Cell___init__.__redef.apply(this,arguments); };
		
		var x = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.x===undefined))?	1 :   typeof(_kwargs_)=='object'?_kwargs_.x: __invalid_call__('function `__init__` requires named keyword arguments, invalid parameter for `x`',arguments);
		this.x = x;
	}/*end->	`__init__`	*/

	a =  new Cell({ x:2 });
	if (!(a.x === 2)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [attr.py](class/attr.py)

input:
------
```python
from runtime import *
"""instance and class attributes"""

class A:
    g = 6
    def __init__(self):
        self.b = 5

a = None
def main():
    a = A()

    assert(a.b == 5)

    ## this is valid in regular CPython, but not in PythonJS,
    ## the variable `g` is only attached to the class Object,
    ## not the instance.  The builtin `getattr` is smart enough
    ## to check the class object for the attribute, and return
    ## it if it finds it on the class.
    #assert(a.g == 6)

    try:
        x = a.c
        assert(not 'No exception: on undefined attribute')
    except AttributeError:
        pass

    b = a
    assert(getattr(b, 'b') == 5)
    assert(getattr(b, 'g') == 6)
    try:
        getattr(b, 'c')
        assert(not 'No exception: getattr on undefined attribute')
    except AttributeError:
        pass

    b.g = 100
    assert( A.g == 6)
main()
```
output:
------
```javascript


var A =  function A()
{
/***/ if (A.__recompile !== undefined) { eval("A.__redef="+A.__recompile); A.__recompile=undefined; };
/***/ if (A.__redef !== undefined) { return A.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
	/***/ try {
	this.__init__();
	/***/ } catch (__err) { if (__debugger__.onerror(__err, A, this.__init__)==true){debugger;}else{throw __err;} };
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
/***/ if (A_toString.__recompile !== undefined) { eval("A_toString.__redef="+A_toString.__recompile); A_toString.__recompile=undefined; };
/***/ if (A_toString.__redef !== undefined) { return A_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

A.prototype.__init__ =  function A___init__()
{
/***/ if (A___init__.__recompile !== undefined) { eval("A___init__.__redef="+A___init__.__recompile); A___init__.__recompile=undefined; };
/***/ if (A___init__.__redef !== undefined) { return A___init__.__redef.apply(this,arguments); };
	
	this.b = 5;
}/*end->	`__init__`	*/

A.g = 6;
a = null;
var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,x,b;
	a =  new A();
	if (!(a.b === 5)) {throw new Error("assertion failed"); }
		try {
x = a.c;
if (!(! ("No exception: on undefined attribute"))) {throw new Error("assertion failed"); }
	} catch(__exception__) {
if (__exception__ == AttributeError || __exception__ instanceof AttributeError) {
/*pass*/
}

}
	b = a;
	if (!(getattr(b, "b") === 5)) {throw new Error("assertion failed"); }
	if (!(getattr(b, "g") === 6)) {throw new Error("assertion failed"); }
		try {
getattr(b, "c");
if (!(! ("No exception: getattr on undefined attribute"))) {throw new Error("assertion failed"); }
	} catch(__exception__) {
if (__exception__ == AttributeError || __exception__ instanceof AttributeError) {
/*pass*/
}

}
	b.g = 100;
	if (!(A.g === 6)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [simple.py](class/simple.py)

input:
------
```python
from runtime import *
"""simple class"""

class A:
    def __init__(self):
        self.x = 5

def main():
    a = A()
    assert(a.x == 5)

main()
```
output:
------
```javascript


var A =  function A()
{
/***/ if (A.__recompile !== undefined) { eval("A.__redef="+A.__recompile); A.__recompile=undefined; };
/***/ if (A.__redef !== undefined) { return A.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
	/***/ try {
	this.__init__();
	/***/ } catch (__err) { if (__debugger__.onerror(__err, A, this.__init__)==true){debugger;}else{throw __err;} };
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
/***/ if (A_toString.__recompile !== undefined) { eval("A_toString.__redef="+A_toString.__recompile); A_toString.__recompile=undefined; };
/***/ if (A_toString.__redef !== undefined) { return A_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

A.prototype.__init__ =  function A___init__()
{
/***/ if (A___init__.__recompile !== undefined) { eval("A___init__.__redef="+A___init__.__recompile); A___init__.__recompile=undefined; };
/***/ if (A___init__.__redef !== undefined) { return A___init__.__redef.apply(this,arguments); };
	
	this.x = 5;
}/*end->	`__init__`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a;
	a =  new A();
	if (!(a.x === 5)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [__add__.py](class/__add__.py)

input:
------
```python
from runtime import *
"""custom addition"""

class A:
	def __init__(self):
		self.x = 5
	def __add__(self, other):
		return self.x + other.x


def main():
	print 'testing __add__ operator overloading'
	a = A()
	b = A()
	with oo:
		c = a + b
	assert( c == 10 )
	print 'ok'

main()
```
output:
------
```javascript


var A =  function A()
{
/***/ if (A.__recompile !== undefined) { eval("A.__redef="+A.__recompile); A.__recompile=undefined; };
/***/ if (A.__redef !== undefined) { return A.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
	/***/ try {
	this.__init__();
	/***/ } catch (__err) { if (__debugger__.onerror(__err, A, this.__init__)==true){debugger;}else{throw __err;} };
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
/***/ if (A_toString.__recompile !== undefined) { eval("A_toString.__redef="+A_toString.__recompile); A_toString.__recompile=undefined; };
/***/ if (A_toString.__redef !== undefined) { return A_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

A.prototype.__init__ =  function A___init__()
{
/***/ if (A___init__.__recompile !== undefined) { eval("A___init__.__redef="+A___init__.__recompile); A___init__.__recompile=undefined; };
/***/ if (A___init__.__redef !== undefined) { return A___init__.__redef.apply(this,arguments); };
	
	this.x = 5;
}/*end->	`__init__`	*/

A.prototype.__add__ =  function A___add__(other)
{
/***/ if (A___add__.__recompile !== undefined) { eval("A___add__.__redef="+A___add__.__recompile); A___add__.__recompile=undefined; };
/***/ if (A___add__.__redef !== undefined) { return A___add__.__redef.apply(this,arguments); };
	
	return (this.x + other.x);
}/*end->	`__add__`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b;
	console.log("testing __add__ operator overloading");
	a =  new A();
	b =  new A();
	c = (a.__add__(b));
	if (!(c === 10)) {throw new Error("assertion failed"); }
	console.log("ok");
}/*end->	`main`	*/

main();
```
* [mi.py](class/mi.py)

input:
------
```python
from runtime import *
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
		a = self.foo()
		a += self.bar()
		return a

	## extend foo ##
	def foo(self) -> int:
		#a = A.foo(self)  ## TODO fix me, or support `super`
		a  = A.prototype.foo(self)  ## workaround
		a += 100
		return a

def main():
	a = A()
	assert( a.foo()==1 )
	b = B()
	assert( b.bar()==2 )

	c = C()
	assert( c.foo()==101 )
	assert( c.bar()==2 )

	assert( c.call_foo_bar()==103 )

main()
```
output:
------
```javascript


var A =  function A()
{
/***/ if (A.__recompile !== undefined) { eval("A.__redef="+A.__recompile); A.__recompile=undefined; };
/***/ if (A.__redef !== undefined) { return A.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
/***/ if (A_toString.__recompile !== undefined) { eval("A_toString.__redef="+A_toString.__recompile); A_toString.__recompile=undefined; };
/***/ if (A_toString.__redef !== undefined) { return A_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

A.prototype.foo =  function A_foo()
{
/***/ if (A_foo.__recompile !== undefined) { eval("A_foo.__redef="+A_foo.__recompile); A_foo.__recompile=undefined; };
/***/ if (A_foo.__redef !== undefined) { return A_foo.__redef.apply(this,arguments); };
	
	return 1;
}/*end->	`foo`	*/
A.prototype.foo.returns = "int";

var B =  function B()
{
/***/ if (B.__recompile !== undefined) { eval("B.__redef="+B.__recompile); B.__recompile=undefined; };
/***/ if (B.__redef !== undefined) { return B.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`B`	*/

B.prototype.__class__ = B;
B.__name__ = "B";
B.__bases__ = [];
B.prototype.toString =  function B_toString()
{
/***/ if (B_toString.__recompile !== undefined) { eval("B_toString.__redef="+B_toString.__recompile); B_toString.__recompile=undefined; };
/***/ if (B_toString.__redef !== undefined) { return B_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

B.prototype.bar =  function B_bar()
{
/***/ if (B_bar.__recompile !== undefined) { eval("B_bar.__redef="+B_bar.__recompile); B_bar.__recompile=undefined; };
/***/ if (B_bar.__redef !== undefined) { return B_bar.__redef.apply(this,arguments); };
	
	return 2;
}/*end->	`bar`	*/
B.prototype.bar.returns = "int";

var C =  function C()
{
/***/ if (C.__recompile !== undefined) { eval("C.__redef="+C.__recompile); C.__recompile=undefined; };
/***/ if (C.__redef !== undefined) { return C.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`C`	*/

C.prototype.__class__ = C;
C.__name__ = "C";
C.__bases__ = [];
C.prototype.toString =  function C_toString()
{
/***/ if (C_toString.__recompile !== undefined) { eval("C_toString.__redef="+C_toString.__recompile); C_toString.__recompile=undefined; };
/***/ if (C_toString.__redef !== undefined) { return C_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

C.prototype.call_foo_bar =  function C_call_foo_bar()
{
/***/ if (C_call_foo_bar.__recompile !== undefined) { eval("C_call_foo_bar.__redef="+C_call_foo_bar.__recompile); C_call_foo_bar.__recompile=undefined; };
/***/ if (C_call_foo_bar.__redef !== undefined) { return C_call_foo_bar.__redef.apply(this,arguments); };
	var a;
	a = this.foo();
	if (a instanceof Array || __is_typed_array(a)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
	else { a += this.bar(); }
	return a;
}/*end->	`call_foo_bar`	*/
C.prototype.call_foo_bar.returns = "int";

C.prototype.foo =  function C_foo()
{
/***/ if (C_foo.__recompile !== undefined) { eval("C_foo.__redef="+C_foo.__recompile); C_foo.__recompile=undefined; };
/***/ if (C_foo.__redef !== undefined) { return C_foo.__redef.apply(this,arguments); };
	var a;
	a = A.prototype.foo(this);
	a += 100;
	return a;
}/*end->	`foo`	*/
C.prototype.foo.returns = "int";

for (var n in A.prototype) {  if (!(n in C.prototype)) {    C.prototype[n] = A.prototype[n]  }};
C.__bases__.push(A);
for (var n in B.prototype) {  if (!(n in C.prototype)) {    C.prototype[n] = B.prototype[n]  }};
C.__bases__.push(B);
var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b;
	a =  new A();
	if (!(a.foo() === 1)) {throw new Error("assertion failed"); }
	b =  new B();
	if (!(b.bar() === 2)) {throw new Error("assertion failed"); }
	c =  new C();
	if (!(c.foo() === 101)) {throw new Error("assertion failed"); }
	if (!(c.bar() === 2)) {throw new Error("assertion failed"); }
	if (!(c.call_foo_bar() === 103)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [__call__.py](class/__call__.py)

input:
------
```python
"""custom callable"""
from runtime import *

class A:
	def __init__(self):
		self.x = 5

	def __call__(self):
		print self.x
		return 'XXX'

	def foo(self):
		return self.x


def main():
	print 'testing __call__'
	a = A()
	assert a.x == 5
	assert a() == 'XXX'
	assert a.__call__() == 'XXX'
	assert a.foo() == 5
	assert isinstance(a, A)
	print 'ok'

main()
```
output:
------
```javascript


var A =  function A()
{
/***/ if (A.__recompile !== undefined) { eval("A.__redef="+A.__recompile); A.__recompile=undefined; };
/***/ if (A.__redef !== undefined) { return A.__redef.apply(this,arguments); };
			var __call__ =  function __call__()
	{
/***/ if (__call__.__recompile !== undefined) { eval("__call__.__redef="+__call__.__recompile); __call__.__recompile=undefined; };
/***/ if (__call__.__redef !== undefined) { return __call__.__redef.apply(this,arguments); };
		
		console.log(__call__.x);
		return "XXX";
	}/*end->	`__call__`	*/

	__call__.__$UID$__ = __$UID$__ ++;
	__call__.__init__ = this.__init__;
	__call__.foo = this.foo;
	__call__.__call__ = __call__;
	__call__.__class__ = A;
	/***/ try {
	__call__.__init__();
	/***/ } catch (__err) { if (__debugger__.onerror(__err, A, __call__.__init__)==true){debugger;}else{throw __err;} };
	return __call__;
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
/***/ if (A_toString.__recompile !== undefined) { eval("A_toString.__redef="+A_toString.__recompile); A_toString.__recompile=undefined; };
/***/ if (A_toString.__redef !== undefined) { return A_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

A.prototype.__init__ =  function A___init__()
{
/***/ if (A___init__.__recompile !== undefined) { eval("A___init__.__redef="+A___init__.__recompile); A___init__.__recompile=undefined; };
/***/ if (A___init__.__redef !== undefined) { return A___init__.__redef.apply(this,arguments); };
	
	this.x = 5;
}/*end->	`__init__`	*/

A.prototype.foo =  function A_foo()
{
/***/ if (A_foo.__recompile !== undefined) { eval("A_foo.__redef="+A_foo.__recompile); A_foo.__recompile=undefined; };
/***/ if (A_foo.__redef !== undefined) { return A_foo.__redef.apply(this,arguments); };
	
	return this.x;
}/*end->	`foo`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a;
	console.log("testing __call__");
	a =  new A();
	if (!(a.x === 5)) {throw new Error("assertion failed"); }
	if (!(a() === "XXX")) {throw new Error("assertion failed"); }
	if (!(a.__call__() === "XXX")) {throw new Error("assertion failed"); }
	if (!(a.foo() === 5)) {throw new Error("assertion failed"); }
	if (!(isinstance(a, A))) {throw new Error("assertion failed"); }
	console.log("ok");
}/*end->	`main`	*/

main();
```
* [mi_override.py](class/mi_override.py)

input:
------
```python
from runtime import *
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
		a = self.foo()
		a += self.bar()
		return a

	## override foo ##
	def foo(self) -> int:
		return 100

def main():
	a = A()
	assert( a.foo()==1 )
	b = B()
	assert( b.bar()==2 )

	c = C()
	assert( c.foo()==100 )
	assert( c.bar()==2 )

	assert( c.call_foo_bar()==102 )

main()
```
output:
------
```javascript


var A =  function A()
{
/***/ if (A.__recompile !== undefined) { eval("A.__redef="+A.__recompile); A.__recompile=undefined; };
/***/ if (A.__redef !== undefined) { return A.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
/***/ if (A_toString.__recompile !== undefined) { eval("A_toString.__redef="+A_toString.__recompile); A_toString.__recompile=undefined; };
/***/ if (A_toString.__redef !== undefined) { return A_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

A.prototype.foo =  function A_foo()
{
/***/ if (A_foo.__recompile !== undefined) { eval("A_foo.__redef="+A_foo.__recompile); A_foo.__recompile=undefined; };
/***/ if (A_foo.__redef !== undefined) { return A_foo.__redef.apply(this,arguments); };
	
	return 1;
}/*end->	`foo`	*/
A.prototype.foo.returns = "int";

var B =  function B()
{
/***/ if (B.__recompile !== undefined) { eval("B.__redef="+B.__recompile); B.__recompile=undefined; };
/***/ if (B.__redef !== undefined) { return B.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`B`	*/

B.prototype.__class__ = B;
B.__name__ = "B";
B.__bases__ = [];
B.prototype.toString =  function B_toString()
{
/***/ if (B_toString.__recompile !== undefined) { eval("B_toString.__redef="+B_toString.__recompile); B_toString.__recompile=undefined; };
/***/ if (B_toString.__redef !== undefined) { return B_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

B.prototype.bar =  function B_bar()
{
/***/ if (B_bar.__recompile !== undefined) { eval("B_bar.__redef="+B_bar.__recompile); B_bar.__recompile=undefined; };
/***/ if (B_bar.__redef !== undefined) { return B_bar.__redef.apply(this,arguments); };
	
	return 2;
}/*end->	`bar`	*/
B.prototype.bar.returns = "int";

var C =  function C()
{
/***/ if (C.__recompile !== undefined) { eval("C.__redef="+C.__recompile); C.__recompile=undefined; };
/***/ if (C.__redef !== undefined) { return C.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`C`	*/

C.prototype.__class__ = C;
C.__name__ = "C";
C.__bases__ = [];
C.prototype.toString =  function C_toString()
{
/***/ if (C_toString.__recompile !== undefined) { eval("C_toString.__redef="+C_toString.__recompile); C_toString.__recompile=undefined; };
/***/ if (C_toString.__redef !== undefined) { return C_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

C.prototype.call_foo_bar =  function C_call_foo_bar()
{
/***/ if (C_call_foo_bar.__recompile !== undefined) { eval("C_call_foo_bar.__redef="+C_call_foo_bar.__recompile); C_call_foo_bar.__recompile=undefined; };
/***/ if (C_call_foo_bar.__redef !== undefined) { return C_call_foo_bar.__redef.apply(this,arguments); };
	var a;
	a = this.foo();
	if (a instanceof Array || __is_typed_array(a)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
	else { a += this.bar(); }
	return a;
}/*end->	`call_foo_bar`	*/
C.prototype.call_foo_bar.returns = "int";

C.prototype.foo =  function C_foo()
{
/***/ if (C_foo.__recompile !== undefined) { eval("C_foo.__redef="+C_foo.__recompile); C_foo.__recompile=undefined; };
/***/ if (C_foo.__redef !== undefined) { return C_foo.__redef.apply(this,arguments); };
	
	return 100;
}/*end->	`foo`	*/
C.prototype.foo.returns = "int";

for (var n in A.prototype) {  if (!(n in C.prototype)) {    C.prototype[n] = A.prototype[n]  }};
C.__bases__.push(A);
for (var n in B.prototype) {  if (!(n in C.prototype)) {    C.prototype[n] = B.prototype[n]  }};
C.__bases__.push(B);
var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b;
	a =  new A();
	if (!(a.foo() === 1)) {throw new Error("assertion failed"); }
	b =  new B();
	if (!(b.bar() === 2)) {throw new Error("assertion failed"); }
	c =  new C();
	if (!(c.foo() === 100)) {throw new Error("assertion failed"); }
	if (!(c.bar() === 2)) {throw new Error("assertion failed"); }
	if (!(c.call_foo_bar() === 102)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [__mul__.py](class/__mul__.py)

input:
------
```python
from runtime import *
"""custom multiplication"""

class A:
	def __init__(self):
		self.x = 5
	def __mul__(self, other):
		return self.x * other.x


def main():
	a = A()
	b = A()
	with operator_overloading:
		c = a * b
	assert( c == 25 )


main()
```
output:
------
```javascript


var A =  function A()
{
/***/ if (A.__recompile !== undefined) { eval("A.__redef="+A.__recompile); A.__recompile=undefined; };
/***/ if (A.__redef !== undefined) { return A.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
	/***/ try {
	this.__init__();
	/***/ } catch (__err) { if (__debugger__.onerror(__err, A, this.__init__)==true){debugger;}else{throw __err;} };
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
/***/ if (A_toString.__recompile !== undefined) { eval("A_toString.__redef="+A_toString.__recompile); A_toString.__recompile=undefined; };
/***/ if (A_toString.__redef !== undefined) { return A_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

A.prototype.__init__ =  function A___init__()
{
/***/ if (A___init__.__recompile !== undefined) { eval("A___init__.__redef="+A___init__.__recompile); A___init__.__recompile=undefined; };
/***/ if (A___init__.__redef !== undefined) { return A___init__.__redef.apply(this,arguments); };
	
	this.x = 5;
}/*end->	`__init__`	*/

A.prototype.__mul__ =  function A___mul__(other)
{
/***/ if (A___mul__.__recompile !== undefined) { eval("A___mul__.__redef="+A___mul__.__recompile); A___mul__.__recompile=undefined; };
/***/ if (A___mul__.__redef !== undefined) { return A___mul__.__redef.apply(this,arguments); };
	
	return (this.x * other.x);
}/*end->	`__mul__`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b;
	a =  new A();
	b =  new A();
	c = (a.__mul__(b));
	if (!(c === 25)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```