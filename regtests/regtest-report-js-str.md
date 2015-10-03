JavaScript Backend Regression Tests - str
-----------------------------
the following tests compiled, and run in nodejs without any errors
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,b;
	arguments.callee.locals.a=a = "abc";
	arguments.callee.locals.b=b = __replace_method(a, "a", "A");
	if (!(b === "Abc")) {throw new Error("assertion failed"); }
	arguments.callee.locals.a=a = "aaa";
	arguments.callee.locals.b=b = __replace_method(a, "a", "A");
	if (!(b === "AAA")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b,e,d,f;
	if (!(len("a") === 1)) {throw new Error("assertion failed"); }
	arguments.callee.locals.a=a = "XYZ";
	if (!(a[0] === "X")) {throw new Error("assertion failed"); }
	if (!(a[(a.length + -1)] === "Z")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(0, 2, undefined) === "XY")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(undefined, 2, undefined) === "XY")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(1, 3, undefined) === "YZ")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(1, undefined, undefined) === "YZ")) {throw new Error("assertion failed"); }
	if (!(a.__getslice__(-3, -1, undefined) === "XY")) {throw new Error("assertion failed"); }
	if (!(a.lower() === "xyz")) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = "abc";
	if (!(b.upper() === "ABC")) {throw new Error("assertion failed"); }
	if (!("A".charCodeAt(0) === 65)) {throw new Error("assertion failed"); }
	if (!(String.fromCharCode(65) === "A")) {throw new Error("assertion failed"); }
	arguments.callee.locals.c=c = __sprintf("%s-%s", ["xxx", "yyy"]);
	if (!(c === "xxx-yyy")) {throw new Error("assertion failed"); }
	arguments.callee.locals.d=d = __split_method("a b c");
	if (!(d[0] === "a")) {throw new Error("assertion failed"); }
	if (!(d[1] === "b")) {throw new Error("assertion failed"); }
	if (!(d[2] === "c")) {throw new Error("assertion failed"); }
	arguments.callee.locals.d=d = "a,b,c".split(",");
	if (!(d[0] === "a")) {throw new Error("assertion failed"); }
	if (!(d[1] === "b")) {throw new Error("assertion failed"); }
	if (!(d[2] === "c")) {throw new Error("assertion failed"); }
	arguments.callee.locals.e=e = __sprintf("x%sx", 1);
	if (!(e === "x1x")) {throw new Error("assertion failed"); }
	arguments.callee.locals.f=f = "x\"y";
	if (!(f[1].charCodeAt(0) === 34)) {throw new Error("assertion failed"); }
	arguments.callee.locals.f=f = "x\"y";
	if (!(f[1].charCodeAt(0) === 34)) {throw new Error("assertion failed"); }
	arguments.callee.locals.f=f = "x'y\"";
	if (!(f[1].charCodeAt(0) === 39)) {throw new Error("assertion failed"); }
	arguments.callee.locals.f=f = "\r";
	if (!(f[0].charCodeAt(0) === 13)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,x,b;
	arguments.callee.locals.a=a = "XYZ";
	arguments.callee.locals.b=b = "XYZ";
	if (!(a === b)) {throw new Error("assertion failed"); }
	arguments.callee.locals.x=x = false;
		if ("a" < "b")
	{
		arguments.callee.locals.x=x = true;
	}
	if (!(x === true)) {throw new Error("assertion failed"); }
	if (!("a" < "b")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,b;
	console.log("testing string multiplication");
	if (!((("hi".__mul__(2))) === "hihi")) {throw new Error("assertion failed"); }
	arguments.callee.locals.a=a = "hi";
	arguments.callee.locals.b=b = (a.__mul__(2));
	if (!(b === "hihi")) {throw new Error("assertion failed"); }
	if (!(a.__mul__(2) === "hihi")) {throw new Error("assertion failed"); }
	console.log("OK");
}/*end->	`main`	*/
main.locals={};

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
/***/ if (C.__recompile !== undefined) { eval("C.__redef="+C.__recompile); C.__recompile=undefined; };
/***/ if (C.__redef !== undefined) { return C.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
	/***/ try {
	this.__init__();
	/***/ } catch (__err) { if (__debugger__.onerror(__err, C, this.__init__)==true){debugger;}else{throw __err;} };
}/*end->	`C`	*/
C.locals={};

C.prototype.__class__ = C;
C.__name__ = "C";
C.__bases__ = [];
C.prototype.toString =  function C_toString()
{
/***/ if (C_toString.__recompile !== undefined) { eval("C_toString.__redef="+C_toString.__recompile); C_toString.__recompile=undefined; };
/***/ if (C_toString.__redef !== undefined) { return C_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/
C.prototype.toString.locals = {};

C.prototype.__init__ =  function C___init__()
{
/***/ if (C___init__.__recompile !== undefined) { eval("C___init__.__redef="+C___init__.__recompile); C___init__.__recompile=undefined; };
/***/ if (C___init__.__redef !== undefined) { return C___init__.__redef.apply(this,arguments); };
	
	this.value = null;
}/*end->	`__init__`	*/
C.prototype.__init__.locals = {};

C.__init__ = function () { return C.prototype.__init__.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c;
	console.log("testing special strings");
	if (!(len("\\") === 1)) {throw new Error("assertion failed"); }
	arguments.callee.locals.a=a = "éè";
	console.log(a);
	if (!(a === ( ("é" + "è") ))) {throw new Error("assertion failed"); }
	arguments.callee.locals.c=c =  new C();
	c.value = "é";
	if (!(c.value === "é")) {throw new Error("assertion failed"); }
	if (!(len("éè") === 2)) {throw new Error("assertion failed"); }
	if (!("éè".__getslice_lowerstep__(undefined, -1) === "èé")) {throw new Error("assertion failed"); }
	console.log("ok");
}/*end->	`main`	*/
main.locals={};

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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a;
	arguments.callee.locals.a=a = "{x}{y}".format({ x:"A", y:"B" });
	if (!(a === "AB")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,b;
	arguments.callee.locals.a=a = __sprintf("%s.%s", ["X", "Y"]);
	if (!(a[0] === "X")) {throw new Error("assertion failed"); }
	if (!(a[1] === ".")) {throw new Error("assertion failed"); }
	if (!(a[2] === "Y")) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = __sprintf("X%sX", 1.1);
	if (!(b === "X1.1X")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [iter.py](str/iter.py)

input:
------
```python
"""string iteration requires wrappingn with `iter(my)`"""
from runtime import *

def main():
	a = list("abc")
	print a
	assert(a[0] == 'a')
	assert(a[1] == 'b')
	assert(a[2] == 'c')
	print '--------'
	b = ['a']
	for chr in iter("xyz"):
		print chr
		b.append(chr)
		print b
	print '--------'
	print b
	assert(b[0] == 'a')
	assert(b[1] == 'x')
	assert(b[2] == 'y')
	assert(b[3] == 'z')

	b = ['a']
	mystr = "xyz"
	for char in iter(mystr):
		print char
		b.append(char)
		print b
	print '--------'
	print b
	assert(b[0] == 'a')
	assert(b[1] == 'x')
	assert(b[2] == 'y')
	assert(b[3] == 'z')

	x = []
	y = [1,2,3]
	## should be faster to call iter(myarr) when myarry is short. 
	## for long arrays use `for v in myarry`
	for v in iter(y):
		x.append(v)
		print v
		print x
	print '--'
	print x

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,x,mystr,b,y;
	arguments.callee.locals.a=a = list("abc");
	console.log(a);
	if (!(a[0] === "a")) {throw new Error("assertion failed"); }
	if (!(a[1] === "b")) {throw new Error("assertion failed"); }
	if (!(a[2] === "c")) {throw new Error("assertion failed"); }
	console.log("--------");
	arguments.callee.locals.b=b = ["a"];
	var __iter0 = "xyz";
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var chr = __iter0[ __n0 ];
		console.log(chr);
		/***/ try {
		b.append(chr);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, b.append)==true){debugger;}else{throw __err;} };
		console.log(b);
	}
	console.log("--------");
	console.log(b);
	if (!(b[0] === "a")) {throw new Error("assertion failed"); }
	if (!(b[1] === "x")) {throw new Error("assertion failed"); }
	if (!(b[2] === "y")) {throw new Error("assertion failed"); }
	if (!(b[3] === "z")) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = ["a"];
	arguments.callee.locals.mystr=mystr = "xyz";
	var __iter0 = mystr;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var char = __iter0[ __n0 ];
		console.log(char);
		/***/ try {
		b.append(char);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, b.append)==true){debugger;}else{throw __err;} };
		console.log(b);
	}
	console.log("--------");
	console.log(b);
	if (!(b[0] === "a")) {throw new Error("assertion failed"); }
	if (!(b[1] === "x")) {throw new Error("assertion failed"); }
	if (!(b[2] === "y")) {throw new Error("assertion failed"); }
	if (!(b[3] === "z")) {throw new Error("assertion failed"); }
	arguments.callee.locals.x=x = [];
	arguments.callee.locals.y=y = [1, 2, 3];
	var __iter0 = y;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var v = __iter0[ __n0 ];
		/***/ try {
		x.append(v);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, x.append)==true){debugger;}else{throw __err;} };
		console.log(v);
		console.log(x);
	}
	console.log("--");
	console.log(x);
}/*end->	`main`	*/
main.locals={};

main();
```