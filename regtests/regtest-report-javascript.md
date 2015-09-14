JavaScript Backend Regression Tests
-----------------------------
the following tests compiled, and run in nodejs without any errors
* [param_name.py](calling/param_name.py)

input:
------
```python
from runtime import *
"""Function call with the name of a parameter without default value"""
def f1(a):
	return a

def f2(a=1, b=2):
	return a + b

def main():
	print 'testing calling named parameters'
	assert f1(10)==10
	assert f2()  ==3
	assert f2(a=100) == 102
	assert f2(b=500) == 501

	## GOTCHA: calling a function that expects a named keyword parameter,
	## and not giving any named parameters is not valid in Rusthon.
	## this works in regular python, but it is bad-style, 
	## and would be slow to support in javascript.
	#assert( f2( 100 ) == 102 )


	## GOTCHA: below is valid in Python, but not in Rusthon,
	## this is bad-style because the caller is enforcing
	## a naming convention on the function, and in typical
	## python code named parameters are only used when
	## the function has been defined with named keywords.
	## allowing this would also allow for bad-style that
	## would break when calling js functions from external libs.
	#assert( f1( a=100 ) == 100 )

	print 'ok'

main()
```
output:
------
```javascript


var f1 =  function f1(a)
{
	
	return a;
}/*end->	`f1`	*/

var f2 =  function f2(_kwargs_)
{
	
	var a = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.a===undefined))?	1 :   typeof(_kwargs_)=='object'?_kwargs_.a: __invalid_call__('function `f2` requires named keyword arguments, invalid parameter for `a`',arguments);
	var b = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.b===undefined))?	2 :   typeof(_kwargs_)=='object'?_kwargs_.b: __invalid_call__('function `f2` requires named keyword arguments, invalid parameter for `b`',arguments);
	return (a + b);
}/*end->	`f2`	*/

var main =  function main()
{
	
	console.log("testing calling named parameters");
	if (!(f1(10) === 10)) {throw new Error("assertion failed"); }
	if (!(f2() === 3)) {throw new Error("assertion failed"); }
	if (!(f2({ a:100 }) === 102)) {throw new Error("assertion failed"); }
	if (!(f2({ b:500 }) === 501)) {throw new Error("assertion failed"); }
	console.log("ok");
}/*end->	`main`	*/

main();
```
* [variable_kwargs_class.py](calling/variable_kwargs_class.py)

input:
------
```python
from runtime import *
"""variable keywords"""
class A:
	def f2(self, **kw):
		a = 0
		for key in kw:
			a += kw[key]
		return a

def main():
	a = A()
	assert( a.f2(x=1,y=2) == 3 )
main()
```
output:
------
```javascript


var A =  function A()
{
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
	return this.__$UID$__;
}/*end->	`toString`	*/

A.prototype.f2 =  function A_f2(kw)
{
	var a;
	a = 0;
	var __iter0 = kw;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var key = __iter0[ __n0 ];
		if (a instanceof Array || __is_typed_array(a)) { a.extend(kw[key]); }
else { a += kw[key]; }
	}
	return a;
}/*end->	`f2`	*/

var main =  function main()
{
	var a;
	a =  new A();
	if (!(a.f2({ x:1, y:2 }) === 3)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [variable_kwargs_class_init.py](calling/variable_kwargs_class_init.py)

input:
------
```python
from runtime import *
"""variable keywords"""
class A:
	def __init__(self, **kw):
		a = 0
		for key in kw:
			a += kw[key]
		self.value = a

def main():
	a = A(x=1,y=2)
	assert( a.value == 3 )
main()
```
output:
------
```javascript


var A =  function A(kw)
{
	this.__$UID$__ = __$UID$__ ++;
	this.__init__(kw);
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
	return this.__$UID$__;
}/*end->	`toString`	*/

A.prototype.__init__ =  function A___init__(kw)
{
	var a;
	a = 0;
	var __iter0 = kw;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var key = __iter0[ __n0 ];
		if (a instanceof Array || __is_typed_array(a)) { a.extend(kw[key]); }
else { a += kw[key]; }
	}
	this.value = a;
}/*end->	`__init__`	*/

var main =  function main()
{
	var a;
	a =  new A({ x:1, y:2 });
	if (!(a.value === 3)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [lambda.py](calling/lambda.py)

input:
------
```python
from runtime import *
"""lambda function"""

def get_lambda():
	return lambda x,y: x+y

def get_lambdas():
	return [lambda a,b: a+b, lambda x,y: x+y]

def call_lambda( F ):
	return F()

def call_lambda2( callback=None ):
	return callback()

def main():
	f = lambda a,b: a+b
	assert( f(1,2) == 3 )

	assert( (lambda a,b: a+b)(1,2) == 3 )

	assert( get_lambda()(1,2) == 3 )

	funcs = get_lambdas()
	assert( funcs[0](1,2) == 3 )
	assert( funcs[1](1,2) == 3 )

	funcs = [lambda a,b: a+b, lambda x,y: x+y]
	assert( funcs[0](1,2) == 3 )
	assert( funcs[1](1,2) == 3 )

	d = { 'x':lambda a,b: a+b }
	assert( d['x'](1,2) == 3 )

	e = ( lambda a,b: a+b, lambda x,y: x+y )
	assert( e[0](1,2) == 3 )
	assert( e[1](1,2) == 3 )

	r = call_lambda( lambda : int(100) )
	assert( r==100 )


	r = call_lambda2( callback = lambda : int(200) )
	assert( r==200 )
main()
```
output:
------
```javascript


var get_lambda =  function get_lambda()
{
	
			var __lambda__ =  function __lambda__(x, y)
	{
		
		return (x + y);
	}/*end->	`__lambda__`	*/

	return __lambda__;
}/*end->	`get_lambda`	*/

var get_lambdas =  function get_lambdas()
{
	
	return [(function (a,b) {return (a + b);}), (function (x,y) {return (x + y);})];
}/*end->	`get_lambdas`	*/

var call_lambda =  function call_lambda(F)
{
	
	return F();
}/*end->	`call_lambda`	*/

var call_lambda2 =  function call_lambda2(_kwargs_)
{
	
	var callback = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.callback===undefined))?	null :   typeof(_kwargs_)=='object'?_kwargs_.callback: __invalid_call__('function `call_lambda2` requires named keyword arguments, invalid parameter for `callback`',arguments);
	return callback();
}/*end->	`call_lambda2`	*/

var main =  function main()
{
	var funcs,r,e,d,f;
			var __lambda__ =  function __lambda__(a, b)
	{
		
		return (a + b);
	}/*end->	`__lambda__`	*/

	f = __lambda__;
	if (!(f(1, 2) === 3)) {throw new Error("assertion failed"); }
	if (!((function (a,b) {return (a + b);})(1, 2) === 3)) {throw new Error("assertion failed"); }
	if (!(get_lambda()(1, 2) === 3)) {throw new Error("assertion failed"); }
	funcs = get_lambdas();
	if (!(funcs[0](1, 2) === 3)) {throw new Error("assertion failed"); }
	if (!(funcs[1](1, 2) === 3)) {throw new Error("assertion failed"); }
	funcs = [(function (a,b) {return (a + b);}), (function (x,y) {return (x + y);})];
	if (!(funcs[0](1, 2) === 3)) {throw new Error("assertion failed"); }
	if (!(funcs[1](1, 2) === 3)) {throw new Error("assertion failed"); }
	d = dict({  }, { copy:false, keytype:"string", iterable:[["x", (function (a,b) {return (a + b);})]] });
	if (!(d["x"](1, 2) === 3)) {throw new Error("assertion failed"); }
	e = [(function (a,b) {return (a + b);}), (function (x,y) {return (x + y);})];
	if (!(e[0](1, 2) === 3)) {throw new Error("assertion failed"); }
	if (!(e[1](1, 2) === 3)) {throw new Error("assertion failed"); }
	r = call_lambda((function () {return int(100);}));
	if (!(r === 100)) {throw new Error("assertion failed"); }
	r = call_lambda2({ callback:(function () {return int(200);}) });
	if (!(r === 200)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [variable_kwargs.py](calling/variable_kwargs.py)

input:
------
```python
from runtime import *
"""variable keywords"""

def f2(**kw):
	a = 0
	for key in kw:
		a += kw[key]
	return a

def main():

	assert( f2(x=1,y=2) == 3 )
main()
```
output:
------
```javascript


var f2 =  function f2(kw)
{
	var a;
	a = 0;
	var __iter0 = kw;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var key = __iter0[ __n0 ];
		if (a instanceof Array || __is_typed_array(a)) { a.extend(kw[key]); }
else { a += kw[key]; }
	}
	return a;
}/*end->	`f2`	*/

var main =  function main()
{
	
	if (!(f2({ x:1, y:2 }) === 3)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [variable_args.py](calling/variable_args.py)

input:
------
```python
from runtime import *
"""variable args"""
def f(a, *args):
	print '*args'
	print args
	c = a
	for b in args:
		c += b
	return c

def main():
	print 'testing calling function that takes *args'
	assert( f(1, 2, 3, 3) == 9)
	print 'ok'

main()
```
output:
------
```javascript


var f =  function f(a)
{
var args = Array.prototype.splice.call(arguments,1, arguments.length);
	var c;
	console.log("*args");
	console.log(args);
	c = a;
	var __iter0 = args;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var b = __iter0[ __n0 ];
		if (c instanceof Array || __is_typed_array(c)) { c.extend(b); }
else { c += b; }
	}
	return c;
}/*end->	`f`	*/

var main =  function main()
{
	
	console.log("testing calling function that takes *args");
	if (!(f(1, 2, 3, 3) === 9)) {throw new Error("assertion failed"); }
	console.log("ok");
}/*end->	`main`	*/

main();
```
* [args.py](calling/args.py)

input:
------
```python
from runtime import *
"""simple function call"""
def f(a, b, c):
	return a+b+c

def main():
	assert( f(1,2,3) == 6)


main()
```
output:
------
```javascript


var f =  function f(a, b, c)
{
	
	return ((a + b) + c);
}/*end->	`f`	*/

var main =  function main()
{
	
	if (!(f(1, 2, 3) === 6)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [keyword.py](calling/keyword.py)

input:
------
```python
from runtime import *
"""keywords"""
def f(a, b=None, c=None):
	return (a+b) * c


def main():
	print 'testing keywords'
	print f(1, b=2, c=3)
	print f(1, c=3, b=2)
	assert( f(1, b=2, c=3) == 9)
	assert( f(1, c=3, b=2) == 9)
	print 'ok'
main()
```
output:
------
```javascript


var f =  function f(a, _kwargs_)
{
	
	var b = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.b===undefined))?	null :   typeof(_kwargs_)=='object'?_kwargs_.b: __invalid_call__('function `f` requires named keyword arguments, invalid parameter for `b`',arguments);
	var c = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.c===undefined))?	null :   typeof(_kwargs_)=='object'?_kwargs_.c: __invalid_call__('function `f` requires named keyword arguments, invalid parameter for `c`',arguments);
	return ((a + b) * c);
}/*end->	`f`	*/

var main =  function main()
{
	
	console.log("testing keywords");
	console.log(f(1, { b:2, c:3 }));
	console.log(f(1, { c:3, b:2 }));
	if (!(f(1, { b:2, c:3 }) === 9)) {throw new Error("assertion failed"); }
	if (!(f(1, { c:3, b:2 }) === 9)) {throw new Error("assertion failed"); }
	console.log("ok");
}/*end->	`main`	*/

main();
```
* [starargs.py](calling/starargs.py)

input:
------
```python
from runtime import *
"""unpack starargs"""
def f(x, a, b, c):
	return x+a+b+c

def f2(x,y,z, w=0):
	return x+y+z+w

def main():
	a = [1,1,1]
	assert( f(1, *a) == 4)

	assert( f2(*a, w=10) == 13)

	b = [1,1]
	assert( f2(100, *b, w=10) == 112)

main()
```
output:
------
```javascript


var f =  function f(x, a, b, c)
{
	
	return (((x + a) + b) + c);
}/*end->	`f`	*/

var f2 =  function f2(x, y, z, _kwargs_)
{
	
	var w = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.w===undefined))?	0 :   typeof(_kwargs_)=='object'?_kwargs_.w: __invalid_call__('function `f2` requires named keyword arguments, invalid parameter for `w`',arguments);
	return (((x + y) + z) + w);
}/*end->	`f2`	*/

var main =  function main()
{
	var a,b;
	a = [1, 1, 1];
	if (!(f.apply(f, [].extend([1]).extend(a)) === 4)) {throw new Error("assertion failed"); }
	if (!(f2.apply(f2, [].extend(a).append({ w:10 })) === 13)) {throw new Error("assertion failed"); }
	b = [1, 1];
	if (!(f2.apply(f2, [].extend([100]).extend(b).append({ w:10 })) === 112)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [replace.py](str/replace.py)

input:
------
```python
"""replace"""
from runtime import *

def main():
	a = 'abc'
	b = a.replace('a', 'A')
	assert( b == 'Abc')

	a = 'aaa'
	b = a.replace('a', 'A')
	assert( b == 'AAA')

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b;
	a = "abc";
	b = __replace_method(a, "a", "A");
	if (!(b === "Abc")) {throw new Error("assertion failed"); }
	a = "aaa";
	b = __replace_method(a, "a", "A");
	if (!(b === "AAA")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [basics.py](str/basics.py)

input:
------
```python
"""string basics"""

from runtime import *

def main():
	assert(len('a') == 1)
	a = 'XYZ'
	assert( a[0] == 'X' )
	assert( a[-1] == 'Z' )
	assert( a[0:2] == 'XY' )
	assert( a[:2] == 'XY' )
	assert( a[1:3] == 'YZ' )
	assert( a[1:] == 'YZ' )
	assert( a[-3:-1] == 'XY' )

	assert( a.lower() == 'xyz' )
	b = 'abc'
	assert( b.upper() == 'ABC' )

	assert( ord('A') == 65 )
	assert( chr(65) == 'A' )

	c = '%s-%s' %('xxx', 'yyy')
	assert( c == 'xxx-yyy' )

	d = 'a b c'.split()
	assert( d[0]=='a' )
	assert( d[1]=='b' )
	assert( d[2]=='c' )

	d = 'a,b,c'.split(',')
	assert( d[0]=='a' )
	assert( d[1]=='b' )
	assert( d[2]=='c' )

	e = 'x%sx' %1
	assert( e=='x1x' )

	f = 'x"y'
	assert( ord(f[1]) == 34 )

	f = 'x\"y'
	assert( ord(f[1]) == 34 )

	f = 'x\'y"'
	assert( ord(f[1]) == 39 )

	f = '\r'
	assert( ord(f[0]) == 13 )

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,c,b,e,d,f;
	if (!(len("a") === 1)) {throw new Error("assertion failed"); }
	a = "XYZ";
	if (!(a[0] === "X")) {throw new Error("assertion failed"); }
	if (!(a[(a.length + -1)] === "Z")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(0, 2, undefined) === "XY")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(undefined, 2, undefined) === "XY")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(1, 3, undefined) === "YZ")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(1, undefined, undefined) === "YZ")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(-3, -1, undefined) === "XY")) {throw new Error("assertion failed"); }
	if (!(a.lower() === "xyz")) {throw new Error("assertion failed"); }
	b = "abc";
	if (!(b.upper() === "ABC")) {throw new Error("assertion failed"); }
	if (!("A".charCodeAt(0) === 65)) {throw new Error("assertion failed"); }
	if (!(String.fromCharCode(65) === "A")) {throw new Error("assertion failed"); }
	c = __sprintf("%s-%s", ["xxx", "yyy"]);
	if (!(c === "xxx-yyy")) {throw new Error("assertion failed"); }
	d = __split_method("a b c");
	if (!(d[0] === "a")) {throw new Error("assertion failed"); }
	if (!(d[1] === "b")) {throw new Error("assertion failed"); }
	if (!(d[2] === "c")) {throw new Error("assertion failed"); }
	d = "a,b,c".split(",");
	if (!(d[0] === "a")) {throw new Error("assertion failed"); }
	if (!(d[1] === "b")) {throw new Error("assertion failed"); }
	if (!(d[2] === "c")) {throw new Error("assertion failed"); }
	e = __sprintf("x%sx", 1);
	if (!(e === "x1x")) {throw new Error("assertion failed"); }
	f = "x\"y";
	if (!(f[1].charCodeAt(0) === 34)) {throw new Error("assertion failed"); }
	f = "x\"y";
	if (!(f[1].charCodeAt(0) === 34)) {throw new Error("assertion failed"); }
	f = "x'y\"";
	if (!(f[1].charCodeAt(0) === 39)) {throw new Error("assertion failed"); }
	f = "\r";
	if (!(f[0].charCodeAt(0) === 13)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [compare.py](str/compare.py)

input:
------
```python
"""compare"""

from runtime import *

def main():
	a = 'XYZ'
	b = 'XYZ'
	assert( a == b )

	x = False
	if 'a' < 'b':
		x = True

	assert( x==True )

	assert( 'a' < 'b' )

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,x,b;
	a = "XYZ";
	b = "XYZ";
	if (!(a === b)) {throw new Error("assertion failed"); }
	x = false;
		if ("a" < "b")
	{
		x = true;
	}
	if (!(x === true)) {throw new Error("assertion failed"); }
	if (!("a" < "b")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [mul.py](str/mul.py)

input:
------
```python
"""string multiplication"""
from runtime import *

def main():
	print 'testing string multiplication'
	assert 'hi'*2 == 'hihi'
	a = 'hi'

	## this fails because `a` is not a string literal,
	## operator overloading must be used for this to work.
	#assert a*2 == 'hihi'

	with oo:
		b = a * 2

	assert( b == 'hihi' )

	## you can also be verbose, and use `__mul__` directly
	assert a.__mul__(2) == 'hihi'
	print 'OK'

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b;
	console.log("testing string multiplication");
	if (!((("hi".__mul__(2))) === "hihi")) {throw new Error("assertion failed"); }
	a = "hi";
	b = (a.__mul__(2));
	if (!(b === "hihi")) {throw new Error("assertion failed"); }
	if (!(a.__mul__(2) === "hihi")) {throw new Error("assertion failed"); }
	console.log("OK");
}/*end->	`main`	*/

main();
```
* [specials.py](str/specials.py)

input:
------
```python
"""Specials chars in strings"""
from runtime import *

class C:
	def __init__(self):
		self.value = None

def main():
	print 'testing special strings'
	assert(len('\\') == 1)
	#a = u'éè'  ## prefixing `u` is invalid, and will cause UnicodeDecodeError

	a = 'éè'
	print a
	assert( a == 'é' + 'è')

	c = C()
	c.value = "é"
	assert( c.value == 'é')

	assert len('éè') == 2
	assert('éè'[::-1] == 'èé')
	print 'ok'

main()
```
output:
------
```javascript


var C =  function C()
{
	this.__$UID$__ = __$UID$__ ++;
	this.__init__();
}/*end->	`C`	*/

C.prototype.__class__ = C;
C.__name__ = "C";
C.__bases__ = [];
C.prototype.toString =  function C_toString()
{
	return this.__$UID$__;
}/*end->	`toString`	*/

C.prototype.__init__ =  function C___init__()
{
	
	this.value = null;
}/*end->	`__init__`	*/

var main =  function main()
{
	var a,c;
	console.log("testing special strings");
	if (!(len("\\") === 1)) {throw new Error("assertion failed"); }
	a = "éè";
	console.log(a);
	if (!(a === ( ("é" + "è") ))) {throw new Error("assertion failed"); }
	c =  new C();
	c.value = "é";
	if (!(c.value === "é")) {throw new Error("assertion failed"); }
	if (!(len("éè") === 2)) {throw new Error("assertion failed"); }
	if (!("éè".__getslice__(undefined, undefined, -1) === "èé")) {throw new Error("assertion failed"); }
	console.log("ok");
}/*end->	`main`	*/

main();
```
* [format.py](str/format.py)

input:
------
```python
"""string.format"""
from runtime import *

def main():
	a = '{x}{y}'.format( x='A', y='B')
	assert(a == 'AB')

main()
```
output:
------
```javascript


var main =  function main()
{
	var a;
	a = "{x}{y}".format({ x:"A", y:"B" });
	if (!(a === "AB")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [sprintf.py](str/sprintf.py)

input:
------
```python
"""sprintf"""
from runtime import *

def main():
	a = '%s.%s' %('X', 'Y')
	assert(a[0] == 'X')
	assert(a[1] == '.')
	assert(a[2] == 'Y')

	b = 'X%sX' %1.1
	assert(b == 'X1.1X')

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b;
	a = __sprintf("%s.%s", ["X", "Y"]);
	if (!(a[0] === "X")) {throw new Error("assertion failed"); }
	if (!(a[1] === ".")) {throw new Error("assertion failed"); }
	if (!(a[2] === "Y")) {throw new Error("assertion failed"); }
	b = __sprintf("X%sX", 1.1);
	if (!(b === "X1.1X")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [iter.py](str/iter.py)

input:
------
```python
"""The string iterator"""
from runtime import *

def main():
	a = list("abc")
	assert(a[0] == 'a')
	assert(a[1] == 'b')
	assert(a[2] == 'c')

	b = ['a']
	for i in "xyz":
		b.append(i)
	assert(b[0] == 'a')
	assert(b[1] == 'x')
	assert(b[2] == 'y')
	assert(b[3] == 'z')

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b;
	a = list("abc");
	if (!(a[0] === "a")) {throw new Error("assertion failed"); }
	if (!(a[1] === "b")) {throw new Error("assertion failed"); }
	if (!(a[2] === "c")) {throw new Error("assertion failed"); }
	b = ["a"];
	var __iter0 = "xyz";
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var i = __iter0[ __n0 ];
		b.append(i);
	}
	if (!(b[0] === "a")) {throw new Error("assertion failed"); }
	if (!(b[1] === "x")) {throw new Error("assertion failed"); }
	if (!(b[2] === "y")) {throw new Error("assertion failed"); }
	if (!(b[3] === "z")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [init.py](dict/init.py)

input:
------
```python
from runtime import *
"""Defined with {}"""
def f():
    pass
class G(object):
	pass

def main():
	g = G()
	a = {2: 22, 3:33, f:44, G:55, g:66}
	assert(a[2] == 22)
	assert(a[3] == 33)
	#assert(a[f] == 44)
	#assert(a[G] == 55)
	#assert(a[g] == 66)

main()
```
output:
------
```javascript


var f =  function f()
{
	
	/*pass*/
}/*end->	`f`	*/

var G =  function G()
{
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`G`	*/

G.prototype.__class__ = G;
G.__name__ = "G";
G.__bases__ = [];
G.prototype.toString =  function G_toString()
{
	return this.__$UID$__;
}/*end->	`toString`	*/

var main =  function main()
{
	var a,g;
	g =  new G();
	a = dict({ f:44, G:55, g:66 }, { copy:false, keytype:"int", iterable:[[2, 22], [3, 33]] });
	if (!(a[2] === 22)) {throw new Error("assertion failed"); }
	if (!(a[3] === 33)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [dict_comprehension.py](dict/dict_comprehension.py)

input:
------
```python
'''
dict comprehensions
'''



def main():
	m = { a:'xxx' for a in range(10)}
	print(m)
```
output:
------
```javascript
var main =  function main()
{
	var m;
	var __comp__0;
	var idx0;
	var iter0;
	var get0;
	__comp__0 = {  };
	idx0 = 0;
	iter0 = 10;
	while (idx0 < iter0)
	{
		var a;
		a = idx0;
		__comp__0[a] = "xxx";
		idx0 ++;
	}
	m = __comp__0;
	console.log(m);
}/*end->	`main`	*/
```
* [if_empty.py](dict/if_empty.py)

input:
------
```python
from runtime import *
"""if empty dict then false"""

## if mydict: will not work,
## workaround: `if len(d.keys())`

def main():
	d = {}
	#print __jsdict_keys(d)
	if d.keys().length:
		err1 = 1
	else:
		err1 = 0

	if len({}.keys()):
		err2 = 1
	else:
		err2 = 0

	d['x'] = 'xxx'
	if len(d.keys()):
		err3 = 0
	else:
		err3 = 1

	assert( err1 == 0 )
	assert( err2 == 0 )
	assert( err3 == 0 )

main()
```
output:
------
```javascript


var main =  function main()
{
	var err3,err2,err1,d;
	d = dict({  }, { copy:false });
		if (__jsdict_keys(d).length)
	{
		err1 = 1;
	}
	else
	{
		err1 = 0;
	}
		if (len(__jsdict_keys(dict({  }, { copy:false }))))
	{
		err2 = 1;
	}
	else
	{
		err2 = 0;
	}
	d["x"] = "xxx";
		if (len(__jsdict_keys(d)))
	{
		err3 = 0;
	}
	else
	{
		err3 = 1;
	}
	if (!(err1 === 0)) {throw new Error("assertion failed"); }
	if (!(err2 === 0)) {throw new Error("assertion failed"); }
	if (!(err3 === 0)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [keys.py](dict/keys.py)

input:
------
```python
from runtime import *
"""dict.keys()"""

def main():
	a = {'foo':'bar'}
	keys = a.keys()
	assert( 'foo' in keys )

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,keys;
	a = dict({  }, { copy:false, keytype:"string", iterable:[["foo", "bar"]] });
	keys = __jsdict_keys(a);
	if (!(__contains__(keys, "foo"))) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [item.py](dict/item.py)

input:
------
```python
from runtime import *
"""__getitem__"""

def f(): pass
class G(object):
	def get(self, x,y=None):
		if y: return y
		else: return x
	def set(self, x,y):
		print 'set method ok'
		print x, y
		return True
	def items(self):
		return True

	def pop(self, x):
		return x

def main():
	g = G()

	## mixing string and number keys in a dict literal
	## is not allowed, and will raise SyntaxError at transpile time.
	#a = {'2': 22, 3:33}

	## this dict has inferred int keys, other key types are not allowed ##
	a = {2: 22, 3:33}

	assert(a[2] == 22)
	assert(a[3] == 33)

	## these raise TypeError at runtime, because the keytypes are invalid
	#a[f] = 44
	#a[g] = 66
	#a[G] = 55
	#assert(a[f] == 44)
	#assert(a[G] == 55)
	#assert(a[g] == 66)

	print a.get(1, 'getok')
	assert a.get('none', 'default') == 'default'
	assert g.get(1)==1
	assert g.get(0, y=2)==2

	a.set(0, 'hi')
	assert a[0]=='hi'

	assert g.set(1,2)
	print 'ok'

	i = a.items()
	print i
	assert len(i)==3

	assert g.items()

	v = a.values()
	print v
	assert len(v)==3

	p = a.pop(2)
	assert p==22
	assert 2 not in a.keys()

	o = a.pop('missing', 'X')
	assert o=='X'

	print a.keys()
	assert a.keys().length == 2

	assert g.pop(100)==100

	print 'testing dict.update'
	u = {1:'x', 2:'y'}
	newkeys = a.update( u )
	print newkeys
	assert 1 in a.keys()
	assert 2 in a.keys()
	assert 'x' in a.values()
	assert 'y' in a.values()

	for newkey in a.update({66:'XXX', 99:'YYY'}):
		print 'new key:' + newkey

	print 'ok'

main()
```
output:
------
```javascript


var f =  function f()
{
	
	/*pass*/
}/*end->	`f`	*/

var G =  function G()
{
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`G`	*/

G.prototype.__class__ = G;
G.__name__ = "G";
G.__bases__ = [];
G.prototype.toString =  function G_toString()
{
	return this.__$UID$__;
}/*end->	`toString`	*/

G.prototype.get =  function G_get(x, _kwargs_)
{
	
	var y = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.y===undefined))?	null :   typeof(_kwargs_)=='object'?_kwargs_.y: __invalid_call__('function `get` requires named keyword arguments, invalid parameter for `y`',arguments);
		if (y)
	{
		return y;
	}
	else
	{
		return x;
	}
}/*end->	`get`	*/

G.prototype.set =  function G_set(x, y)
{
	
	console.log("set method ok");
	console.log([x, y]);
	return true;
}/*end->	`set`	*/

G.prototype.items =  function G_items()
{
	
	return true;
}/*end->	`items`	*/

G.prototype.pop =  function G_pop(x)
{
	
	return x;
}/*end->	`pop`	*/

var main =  function main()
{
	var a,newkeys,g,i,o,p,u,v;
	g =  new G();
	a = dict({  }, { copy:false, keytype:"int", iterable:[[2, 22], [3, 33]] });
	if (!(a[2] === 22)) {throw new Error("assertion failed"); }
	if (!(a[3] === 33)) {throw new Error("assertion failed"); }
	console.log(__jsdict_get(a, 1, "getok"));
	if (!(__jsdict_get(a, "none", "default") === "default")) {throw new Error("assertion failed"); }
	if (!(__jsdict_get(g, 1) === 1)) {throw new Error("assertion failed"); }
	if (!(g.get(0, { y:2 }) === 2)) {throw new Error("assertion failed"); }
	__jsdict_set(a, 0, "hi");
	if (!(a[0] === "hi")) {throw new Error("assertion failed"); }
	if (!(__jsdict_set(g, 1, 2))) {throw new Error("assertion failed"); }
	console.log("ok");
	i = __jsdict_items(a);
	console.log(i);
	if (!(len(i) === 3)) {throw new Error("assertion failed"); }
	if (!(__jsdict_items(g))) {throw new Error("assertion failed"); }
	v = __jsdict_values(a);
	console.log(v);
	if (!(len(v) === 3)) {throw new Error("assertion failed"); }
	p = __jsdict_pop(a, 2);
	if (!(p === 22)) {throw new Error("assertion failed"); }
	if (!(! (__contains__(__jsdict_keys(a), 2)))) {throw new Error("assertion failed"); }
	o = __jsdict_pop(a, "missing", "X");
	if (!(o === "X")) {throw new Error("assertion failed"); }
	console.log(__jsdict_keys(a));
	if (!(__jsdict_keys(a).length === 2)) {throw new Error("assertion failed"); }
	if (!(__jsdict_pop(g, 100) === 100)) {throw new Error("assertion failed"); }
	console.log("testing dict.update");
	u = dict({  }, { copy:false, keytype:"int", iterable:[[1, "x"], [2, "y"]] });
	newkeys = __jsdict_update(a, u);
	console.log(newkeys);
	if (!(__contains__(__jsdict_keys(a), 1))) {throw new Error("assertion failed"); }
	if (!(__contains__(__jsdict_keys(a), 2))) {throw new Error("assertion failed"); }
	if (!(__contains__(__jsdict_values(a), "x"))) {throw new Error("assertion failed"); }
	if (!(__contains__(__jsdict_values(a), "y"))) {throw new Error("assertion failed"); }
	var __iter0 = __jsdict_update(a, dict({  }, { copy:false, keytype:"int", iterable:[[66, "XXX"], [99, "YYY"]] }));
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var newkey = __iter0[ __n0 ];
		console.log(("new key:" + newkey));
	}
	console.log("ok");
}/*end->	`main`	*/

main();
```
* [contains.py](dict/contains.py)

input:
------
```python
from runtime import *
"""key in dict"""

def main():
	## mixing string keys and number keys in a dict literal
	## is allowed in python, but not in Rusthon
	#a = {'2': 22, 3:33}
	#assert( '2' in a )
	#assert( 3 in a )

	a = {2: 22, 3:33}
	assert( 2 in a )
	assert( 3 in a )


main()
```
output:
------
```javascript


var main =  function main()
{
	var a;
	a = dict({  }, { copy:false, keytype:"int", iterable:[[2, 22], [3, 33]] });
	if (!(__contains__(a, 2))) {throw new Error("assertion failed"); }
	if (!(__contains__(a, 3))) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [for_loop.py](loop/for_loop.py)

input:
------
```python
from runtime import *
'''
for loop tests
'''

def main():

	a = [1,2,3]
	y = 0
	for x in a:
		y += x
	assert( y==6 )

	z = ''
	arr = ['a', 'b', 'c']
	for v in arr:
		z += v
	assert( z == 'abc' )

	b = False
	if 'a' in arr:
		b = True
	assert( b == True )

	s = 'hello world'
	z = ''
	for char in s:
		z += char
	assert( z == 'hello world' )

	b = False
	if 'hello' in s:
		b = True
	assert( b==True )

	print 'testing for loop over dict'
	ob = {'a' : 'A', 'b' : 'B'}
	k = ''
	v = ''
	for key in ob:
		k += key
		v += ob[key]
	print k
	print v
	assert(k=='ab' or k=='ba')
	assert(v=='AB' or v=='BA')

	keys = []
	values = []
	for x,y in ob.items():
		keys.append( x )
		values.append( y )

	assert( 'a' in keys )
	assert( 'A' in values )

	ob2 = {'c':'C', 'd':'D'}
	e = 0
	arr = []
	for x,y in ob.items():
		arr.append(x)
		arr.append(y)
		for w,z in ob2.items():
			e += 1
			arr.append(w)
			arr.append(z)

	assert( e==4 )
	assert( 'a' in arr)
	assert( 'b' in arr)
	assert( 'A' in arr)
	assert( 'B' in arr)
	assert( 'c' in arr)
	assert( 'C' in arr)
	assert( 'd' in arr)
	assert( 'D' in arr)



main()
```
output:
------
```javascript


var main =  function main()
{
	var a,arr,b,e,keys,k,ob,s,values,v,y,z,ob2;
	a = [1, 2, 3];
	y = 0;
	var __iter0 = a;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var x = __iter0[ __n0 ];
		if (y instanceof Array || __is_typed_array(y)) { y.extend(x); }
else { y += x; }
	}
	if (!(y === 6)) {throw new Error("assertion failed"); }
	z = "";
	arr = ["a", "b", "c"];
	var __iter0 = arr;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var v = __iter0[ __n0 ];
		if (z instanceof Array || __is_typed_array(z)) { z.extend(v); }
else { z += v; }
	}
	if (!(z === "abc")) {throw new Error("assertion failed"); }
	b = false;
		if (__contains__(arr, "a"))
	{
		b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	s = "hello world";
	z = "";
	var __iter0 = s;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var char = __iter0[ __n0 ];
		if (z instanceof Array || __is_typed_array(z)) { z.extend(char); }
else { z += char; }
	}
	if (!(z === "hello world")) {throw new Error("assertion failed"); }
	b = false;
		if (__contains__(s, "hello"))
	{
		b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	console.log("testing for loop over dict");
	ob = dict({  }, { copy:false, keytype:"string", iterable:[["a", "A"], ["b", "B"]] });
	k = "";
	v = "";
	var __iter0 = ob;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var key = __iter0[ __n0 ];
		if (k instanceof Array || __is_typed_array(k)) { k.extend(key); }
else { k += key; }
		if (v instanceof Array || __is_typed_array(v)) { v.extend(ob[key]); }
else { v += ob[key]; }
	}
	console.log(k);
	console.log(v);
	if (!((k === "ab" || k === "ba"))) {throw new Error("assertion failed"); }
	if (!((v === "AB" || v === "BA"))) {throw new Error("assertion failed"); }
	keys = [];
	values = [];
	var __mtarget__4,x;
	var __iter0 = __jsdict_items(ob);
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var __mtarget__4 = __iter0[ __n0 ];
		x = __mtarget__4[0];
		y = __mtarget__4[1];
		keys.append(x);
		values.append(y);
	}
	if (!(__contains__(keys, "a"))) {throw new Error("assertion failed"); }
	if (!(__contains__(values, "A"))) {throw new Error("assertion failed"); }
	ob2 = dict({  }, { copy:false, keytype:"string", iterable:[["c", "C"], ["d", "D"]] });
	e = 0;
	arr = [];
	var __mtarget__5;
	var __iter0 = __jsdict_items(ob);
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var __mtarget__5 = __iter0[ __n0 ];
		x = __mtarget__5[0];
		y = __mtarget__5[1];
		arr.append(x);
		arr.append(y);
		var __mtarget__6,w;
		var __iter1 = __jsdict_items(ob2);
		if (! (__iter1 instanceof Array || typeof __iter1 == "string" || __is_typed_array(__iter1) || __is_some_array(__iter1) )) { __iter1 = __object_keys__(__iter1) }
		for (var __n1 = 0; __n1 < __iter1.length; __n1++) {
			var __mtarget__6 = __iter1[ __n1 ];
			w = __mtarget__6[0];
			z = __mtarget__6[1];
			e ++;
			arr.append(w);
			arr.append(z);
		}
	}
	if (!(e === 4)) {throw new Error("assertion failed"); }
	if (!(__contains__(arr, "a"))) {throw new Error("assertion failed"); }
	if (!(__contains__(arr, "b"))) {throw new Error("assertion failed"); }
	if (!(__contains__(arr, "A"))) {throw new Error("assertion failed"); }
	if (!(__contains__(arr, "B"))) {throw new Error("assertion failed"); }
	if (!(__contains__(arr, "c"))) {throw new Error("assertion failed"); }
	if (!(__contains__(arr, "C"))) {throw new Error("assertion failed"); }
	if (!(__contains__(arr, "d"))) {throw new Error("assertion failed"); }
	if (!(__contains__(arr, "D"))) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [range.py](loop/range.py)

input:
------
```python
from runtime import *
'''
range builtin
'''

def main():
	a = range(10)
	assert( a[0]==0 )
	assert( a[1]==1 )
	assert( len(a)==10 )

	b = range(1,10)
	assert( b[0]==1 )
	assert( b[1]==2 )
	assert( len(b)==9 )

	c = 0
	for i in range(10):
		c += 1
	assert( c == 10 )

	d = 0
	for i in range(1, 10):
		d += 1
	assert( d == 9 )

	e = 0
	for i in range(1, 8+2):
		e += 1
	assert( e == 9 )

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,c,b,e,d;
	a = range(10);
	if (!(a[0] === 0)) {throw new Error("assertion failed"); }
	if (!(a[1] === 1)) {throw new Error("assertion failed"); }
	if (!(len(a) === 10)) {throw new Error("assertion failed"); }
	b = range(1, 10);
	if (!(b[0] === 1)) {throw new Error("assertion failed"); }
	if (!(b[1] === 2)) {throw new Error("assertion failed"); }
	if (!(len(b) === 9)) {throw new Error("assertion failed"); }
	c = 0;
	var i,i__end__;
	i = 0;
	while (i < 10)
	{
		c ++;
		i += 1;
	}
	if (!(c === 10)) {throw new Error("assertion failed"); }
	d = 0;
	
	i = 1;
	while (i < 10)
	{
		d ++;
		i += 1;
	}
	if (!(d === 9)) {throw new Error("assertion failed"); }
	e = 0;
	
	i = 1;
	i__end__ = (8 + 2);
	while (i < i__end__)
	{
		e ++;
		i += 1;
	}
	if (!(e === 9)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [while.py](loop/while.py)

input:
------
```python
from runtime import *
'''
while loop
'''

arr1 = []
arr2 = []

def main():
	a = 0
	i = 0
	while i < 10:
		j = 0
		while j < 10:
			a += 1
			j += 1
		i += 1

	assert( a==100 )

	while len(arr1)+len(arr2) < 10:
		arr1.append( 1 )
		arr2.append( 2 )

	assert( len(arr1)==5 )
	assert( len(arr2)==5 )

main()
```
output:
------
```javascript


arr1 = [];
arr2 = [];
var main =  function main()
{
	var a,i,j;
	a = 0;
	i = 0;
	while (i < 10)
	{
		j = 0;
		while (j < 10)
		{
			a ++;
			j ++;
		}
		i ++;
	}
	if (!(a === 100)) {throw new Error("assertion failed"); }
	while (((len(arr1) + len(arr2))) < 10)
	{
		arr1.append(1);
		arr2.append(2);
	}
	if (!(len(arr1) === 5)) {throw new Error("assertion failed"); }
	if (!(len(arr2) === 5)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [switch.py](lang/switch.py)

input:
------
```python
from runtime import *
'''
switch case default
'''

def main():
	## this is ok in rust because it can infer the type of x from below,
	## but this fails with the C++ backend because None becomes std::nullptr
	#x = None
	x = ''
	a = 2
	switch a:
		case 1:
			x = 'fail'
		case 2:
			x = 'ok'
		default:
			## default x to some string so that rust can see that x is a string in all cases,
			## this is only required if x was initalized to None
			x = 'default'
			break
	print(x)
	assert( x=='ok' )


main()
```
output:
------
```javascript


var main =  function main()
{
	var a,x;
	x = "";
	a = 2;
		switch (a) {
		case 1: {
	x = "fail";
	} break;
		case 2: {
	x = "ok";
	} break;
		default:
	x = "default";
	break;
	}
	console.log(x);
	if (!(x === "ok")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [list_passed_as_arg.py](lang/list_passed_as_arg.py)

input:
------
```python
from runtime import *
'''
list passed to function
'''

def f( l:[]int ):
	l.append(1)

def main():
	a = []int(1,2,3)
	assert( a[0]==1 )
	f( a )
	assert( len(a)==4 )

	b = [ x for x in range(9) ]
	f( b )
	assert( len(b)==10 )

main()
```
output:
------
```javascript


var f =  function f(l)
{
	var l;
	l.append(1);
}/*end->	`f`	*/
f.args = ["[]int"];

var main =  function main()
{
	var a,b;
	a = [1,2,3] /*array of: int*/;
	if (!(a[0] === 1)) {throw new Error("assertion failed"); }
	f(a);
	if (!(len(a) === 4)) {throw new Error("assertion failed"); }
	var __comp__0;
	var idx0;
	var iter0;
	var get0;
	__comp__0 = [];
	idx0 = 0;
	iter0 = 9;
	while (idx0 < iter0)
	{
		var x;
		x = idx0;
		__comp__0.push(x);
		idx0 ++;
	}
	b = __comp__0;
	f(b);
	if (!(len(b) === 10)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [map_passed_as_arg.py](lang/map_passed_as_arg.py)

input:
------
```python
from runtime import *
'''
list passed to function
'''

def f( m:map[string]int ):
	m['x'] = 100

def main():
	a = map[string]int{
		'x' : 1,
		'y' : 2,
		'z' : 3
	}
	assert( a['x']==1 )
	f( a )
	assert( a['x']==100 )
	#assert( len(a)==4 )
main()
```
output:
------
```javascript


var f =  function f(m)
{
	var m;
	m["x"] = 100;
}/*end->	`f`	*/
f.args = ["map[string]int"];

var main =  function main()
{
	var a;
	a = dict({  }, { copy:false, keytype:"string", iterable:[["x", 1], ["y", 2], ["z", 3]] ,valuetype:"int" });
	if (!(a["x"] === 1)) {throw new Error("assertion failed"); }
	f(a);
	if (!(a["x"] === 100)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [inline.py](lang/inline.py)

input:
------
```python
"""inline"""

def main():
	JS("now = new Date()")
	inline("now = new Date()")
```
output:
------
```javascript
var main =  function main()
{
	
	now = new Date();
	now = new Date();
}/*end->	`main`	*/
```
* [try_except.py](lang/try_except.py)

input:
------
```python
from runtime import *
'''
try except
'''

def main():
	a = [1,2,3]
	b = False
	try:
		a.no_such_method()
		b = 'this should not happen'
	except:
		b = True
	assert( b == True )


main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b;
	a = [1, 2, 3];
	b = false;
		try {
a.no_such_method();
b = "this should not happen";
	} catch(__exception__) {
b = true;

}
	if (!(b === true)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [if_not.py](lang/if_not.py)

input:
------
```python
from runtime import *
"""if not"""

def main():
	a = False
	b = False
	if not a:
		b = True

	assert( b == True )

	a = 0
	b = False
	if not a:
		b = True

	assert( b == True )

	a = 0.0
	b = False
	if not a:
		b = True

	assert( b == True )

	a = None
	b = False
	if not a:
		b = True

	assert( b == True )

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b;
	a = false;
	b = false;
		if (! (a))
	{
		b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	a = 0;
	b = false;
		if (! (a))
	{
		b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	a = 0.0;
	b = false;
		if (! (a))
	{
		b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	a = null;
	b = false;
		if (! (a))
	{
		b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [equality.py](lang/equality.py)

input:
------
```python
from runtime import *
'''
==
'''
# https://github.com/PythonJS/PythonJS/issues/129

def main():
	assert( 0==0 )
	assert( 1==1 )
	assert( 1.0==1 )
	assert('a'=='a')


	a = [6]
	b = [6]
	#t = a==b  ## this works in regular python
	t1 = a.equals(b)
	assert( t1==True )

	a = (6,)
	b = (6,)
	#t = a==b
	t2 = a.equals(b)
	assert( t2==True )

	t3 = ''==0  ## javascript gotcha, workaround: `len('')==0`
	print 'empty string equals zero:' + t3
	#assert( t==False )

	t4 = [1,2].equals([1,2])
	assert( t4==True )

	t5 = ["1","2"].equals([1,2])
	assert( t5==False )


main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b,t4,t5,t2,t3,t1;
	if (!(0 === 0)) {throw new Error("assertion failed"); }
	if (!(1 === 1)) {throw new Error("assertion failed"); }
	if (!(1.0 === 1)) {throw new Error("assertion failed"); }
	if (!("a" === "a")) {throw new Error("assertion failed"); }
	a = [6];
	b = [6];
	t1 = a.equals(b);
	if (!(t1 === true)) {throw new Error("assertion failed"); }
	a = [6];
	b = [6];
	t2 = a.equals(b);
	if (!(t2 === true)) {throw new Error("assertion failed"); }
	t3 = "" === 0;
	console.log(("empty string equals zero:" + t3));
	t4 = [1, 2].equals([1, 2]);
	if (!(t4 === true)) {throw new Error("assertion failed"); }
	t5 = ["1", "2"].equals([1, 2]);
	if (!(t5 === false)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [in.py](lang/in.py)

input:
------
```python
from runtime import *
'''
in (dict contains)
'''

def main():
	d = {'x':1}
	a = 'x' in d
	assert( a==True )
	b = 'y' in d
	assert( b==False )



main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b,d;
	d = dict({  }, { copy:false, keytype:"string", iterable:[["x", 1]] });
	a = __contains__(d, "x");
	if (!(a === true)) {throw new Error("assertion failed"); }
	b = __contains__(d, "y");
	if (!(b === false)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [eval.py](lang/eval.py)

input:
------
```python
from runtime import *
'''
eval
'''

def foo(): return 42
bar = lambda: 42

def main():
	eval('a = bar()') # This one works
	eval('b = foo()') # 'foo' is undefined in normal mode under NodeJS but works in NodeWebkit and Chrome!?
	assert( a==42 )
	assert( b==42 )

main()
```
output:
------
```javascript


var foo =  function foo()
{
	
	return 42;
}/*end->	`foo`	*/

var __lambda__ =  function __lambda__()
{
	
	return 42;
}/*end->	`__lambda__`	*/

bar = __lambda__;
var main =  function main()
{
	
	eval("a = bar()");
	eval("b = foo()");
	if (!(a === 42)) {throw new Error("assertion failed"); }
	if (!(b === 42)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [builtins.py](lang/builtins.py)

input:
------
```python
from runtime import *
'''
builtin functions
'''


def main():
	o = ord('x')
	assert( o == 120 )

	n = float('1.1')
	assert( n==1.1 )

	n = float('NaN')
	print( n )
	assert( isNaN(n)==True )

	r = round( 1.1234, 2)
	print(r)
	assert( str(r) == '1.12' )

	x = chr(120)
	print(x)
	assert x == 'x'

	r = round( 100.001, 2)
	assert( r == 100 )

	i = int( 100.1 )
	assert( i == 100 )

	r = round( 5.49 )
	assert( r == 5 )

	r = round( 5.49, 1 )
	assert( r == 5.5 )


main()
```
output:
------
```javascript


var main =  function main()
{
	var i,x,r,o,n;
	o = "x".charCodeAt(0);
	if (!(o === 120)) {throw new Error("assertion failed"); }
	n = float("1.1");
	if (!(n === 1.1)) {throw new Error("assertion failed"); }
	n = float("NaN");
	console.log(n);
	if (!(isNaN(n) === true)) {throw new Error("assertion failed"); }
	r = round(1.1234, 2);
	console.log(r);
	if (!(str(r) === "1.12")) {throw new Error("assertion failed"); }
	x = String.fromCharCode(120);
	console.log(x);
	if (!(x === "x")) {throw new Error("assertion failed"); }
	r = round(100.001, 2);
	if (!(r === 100)) {throw new Error("assertion failed"); }
	i = int(100.1);
	if (!(i === 100)) {throw new Error("assertion failed"); }
	r = round(5.49);
	if (!(r === 5)) {throw new Error("assertion failed"); }
	r = round(5.49, 1);
	if (!(r === 5.5)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [eval_order.py](lang/eval_order.py)

input:
------
```python
from runtime import *
'''
evaluation order
'''
# https://github.com/PythonJS/PythonJS/issues/131

def main():
	a = False and (False or True)
	assert( a==False )
main()
```
output:
------
```javascript


var main =  function main()
{
	var a;
	a = (false && (false || true));
	if (!(a === false)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [if_else.py](lang/if_else.py)

input:
------
```python
from runtime import *
'''
if/else
'''

#def func(x=None, callback=None):
def func(x:bool=False, callback:lambda()(int)=None ):
	a = False
	if x:   ## can c++ templates support this pythonic style?
		a = False
	else:
		a = True

	assert( a==True )

	a = False
	if callback:
		a = True
	else:
		a = False
	assert( a==True )

def main():
	a = False
	if 1:
		a = True
	assert( a==True )

	a = False
	if False:
		a = False
	else:
		a = True

	assert( a==True )

	a = False
	if None:
		a = False
	else:
		a = True

	assert( a==True )

	cb = lambda : 1+1
	func( callback=cb )



main()
```
output:
------
```javascript


var func =  function func(_kwargs_)
{
	var a;
var callback,x;
	var x        = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.x===undefined))       ?	false :   typeof(_kwargs_)=='object'?_kwargs_.x: __invalid_call__('function `func` requires named keyword arguments, invalid parameter for `x`',arguments);
	var callback = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.callback===undefined))?	null  :   typeof(_kwargs_)=='object'?_kwargs_.callback: __invalid_call__('function `func` requires named keyword arguments, invalid parameter for `callback`',arguments);
	a = false;
		if (x)
	{
		a = false;
	}
	else
	{
		a = true;
	}
	if (!(a === true)) {throw new Error("assertion failed"); }
	a = false;
		if (callback)
	{
		a = true;
	}
	else
	{
		a = false;
	}
	if (!(a === true)) {throw new Error("assertion failed"); }
}/*end->	`func`	*/

var main =  function main()
{
	var a,cb;
	a = false;
		if (1)
	{
		a = true;
	}
	if (!(a === true)) {throw new Error("assertion failed"); }
	a = false;
		if (false)
	{
		a = false;
	}
	else
	{
		a = true;
	}
	if (!(a === true)) {throw new Error("assertion failed"); }
	a = false;
		if (null)
	{
		a = false;
	}
	else
	{
		a = true;
	}
	if (!(a === true)) {throw new Error("assertion failed"); }
			var __lambda__ =  function __lambda__()
	{
		
		return (1 + 1);
	}/*end->	`__lambda__`	*/

	cb = __lambda__;
	func({ callback:cb });
}/*end->	`main`	*/

main();
```
* [new.py](lang/new.py)

input:
------
```python
from runtime import *
'''
js new keyword
'''

def main():
	## new as keyword can be used in simple statements, but can break the parser in some cases,
	## it is only allowed to make it easy to copy and paste js code and convert it to rusthon.
	a = new Date()
	b = new( Date() )  ## using new as a function call is safer and always works
	assert( a.getFullYear()==2015 )
	assert( b.getFullYear()==2015 )

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b;
	a =  new Date();
	b =  new Date();
	if (!(a.getFullYear() === 2015)) {throw new Error("assertion failed"); }
	if (!(b.getFullYear() === 2015)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [raise.py](lang/raise.py)

input:
------
```python
from runtime import *
'''
raise and catch error
'''

def main():
	a = False
	try:
		raise TypeError
	except TypeError:
		a = True

	assert( a==True )

	b = False
	try:
		b = True
	except:
		b = False

	assert( b==True )

	c = False
	try:
		raise AttributeError('name')
	except AttributeError:
		c = True

	assert( c==True )

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,c,b;
	a = false;
		try {
throw new TypeError;
	} catch(__exception__) {
if (__exception__ == TypeError || __exception__ instanceof TypeError) {
a = true;
}

}
	if (!(a === true)) {throw new Error("assertion failed"); }
	b = false;
		try {
b = true;
	} catch(__exception__) {
b = false;

}
	if (!(b === true)) {throw new Error("assertion failed"); }
	c = false;
		try {
throw new AttributeError("name");
	} catch(__exception__) {
if (__exception__ == AttributeError || __exception__ instanceof AttributeError) {
c = true;
}

}
	if (!(c === true)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [issubset.py](set/issubset.py)

input:
------
```python
from runtime import *
"""get/set remote attributes"""

def main():
	x = set([1,2,3])
	y = set([1,2,3,4])

	assert( x.issubset(y)==True )
	assert( y.issubset(x)==False )

	
main()
```
output:
------
```javascript


var main =  function main()
{
	var y,x;
	x = set([1, 2, 3]);
	y = set([1, 2, 3, 4]);
	if (!(x.issubset(y) === true)) {throw new Error("assertion failed"); }
	if (!(y.issubset(x) === false)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```