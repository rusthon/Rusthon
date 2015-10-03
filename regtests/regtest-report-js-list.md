JavaScript Backend Regression Tests - list
-----------------------------
the following tests compiled, and run in nodejs without any errors
* [concatenate.py](list/concatenate.py)

input:
------
```python
from runtime import *
"""concatenate lists"""

def main():
	a = [1,2]
	b = [3,4]
	n = 1
	w = 100
	with oo:
		c = a + b
		## it is slow to just stick everything under `with oo`
		## because these operations on numbers become much slower.
		n += n
		w = w + w

	assert n == 2
	assert w == 200

	assert( len(c)==4 )
	assert( c[0]==1 )
	assert( c[1]==2 )
	assert( c[2]==3 )
	assert( c[3]==4 )

	## the pythonic way is ugly
	d = a.__add__(b)
	assert len(d)==4

	## the recommend way in rusthon
	e = a.add(b)
	assert len(e)==4

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b,e,d,n,w;
	arguments.callee.locals.a=a = [1, 2];
	arguments.callee.locals.b=b = [3, 4];
	arguments.callee.locals.n=n = 1;
	arguments.callee.locals.w=w = 100;
	arguments.callee.locals.c=c = (a.__add__(b));
if (n instanceof Array || __is_typed_array(n)) { n.extend(n); }
	else if (n.__iadd__) { n.__iadd__(n); }
	else { n += n; }
arguments.callee.locals.w=w = (w.__add__(w));
	if (!(n === 2)) {throw new Error("assertion failed"); }
	if (!(w === 200)) {throw new Error("assertion failed"); }
	if (!(len(c) === 4)) {throw new Error("assertion failed"); }
	if (!(c[0] === 1)) {throw new Error("assertion failed"); }
	if (!(c[1] === 2)) {throw new Error("assertion failed"); }
	if (!(c[2] === 3)) {throw new Error("assertion failed"); }
	if (!(c[3] === 4)) {throw new Error("assertion failed"); }
	arguments.callee.locals.d=d = a.__add__(b);
	if (!(len(d) === 4)) {throw new Error("assertion failed"); }
	arguments.callee.locals.e=e = a.add(b);
	if (!(len(e) === 4)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [range.py](list/range.py)

input:
------
```python
from runtime import *
"""range"""
def main():
	a = range(10)
	assert( len(a)==10 )
	assert( a[0] == 0 )
	assert( a[9] == 9 )

	b = range(1,10)
	assert( len(b)==9 )
	assert( b[0] == 1 )
	assert( b[8] == 9 )


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
	arguments.callee.locals.a=a = range(10);
	if (!(len(a) === 10)) {throw new Error("assertion failed"); }
	if (!(a[0] === 0)) {throw new Error("assertion failed"); }
	if (!(a[9] === 9)) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = range(1, 10);
	if (!(len(b) === 9)) {throw new Error("assertion failed"); }
	if (!(b[0] === 1)) {throw new Error("assertion failed"); }
	if (!(b[8] === 9)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [simple.py](list/simple.py)

input:
------
```python
"""basics"""
from runtime import *

def main():
	a = [1,2,3,4]
	assert( len(a)==4 )

	b = list()
	assert( len(b)==0 )
	b.append( 5 )
	assert len(b)==1

	with oo:
		a += b
	assert len(a)==5

	## the pythonic way
	a.extend( b )
	assert len(a)==6

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
	arguments.callee.locals.a=a = [1, 2, 3, 4];
	if (!(len(a) === 4)) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = list();
	if (!(len(b) === 0)) {throw new Error("assertion failed"); }
	/***/ try {
	b.append(5);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, b.append)==true){debugger;}else{throw __err;} };
	if (!(len(b) === 1)) {throw new Error("assertion failed"); }
	if (a instanceof Array || __is_typed_array(a)) { a.extend(b); }
	else if (a.__iadd__) { a.__iadd__(b); }
	else { a += b; }
	if (!(len(a) === 5)) {throw new Error("assertion failed"); }
	/***/ try {
	a.extend(b);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, a.extend)==true){debugger;}else{throw __err;} };
	if (!(len(a) === 6)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [slice.py](list/slice.py)

input:
------
```python
from runtime import *
"""list slice"""

class XXX:
	def __init__(self):
		self.v = range(10)
	def method(self, a):
		return a

def main():
	a = range(10)[:-5]
	assert( len(a)==5 )
	assert( a[4]==4 )

	print '--------'
	b = range(10)[::2]
	print b
	assert( len(b)==5 )
	assert( b[0]==0 )
	assert( b[1]==2 )
	assert( b[2]==4 )
	assert( b[3]==6 )
	assert( b[4]==8 )

	#if BACKEND=='DART':
	#	print(b[...])
	#else:
	#	print(b)


	c = range(20)
	d = c[ len(b) : ]

	#if BACKEND=='DART':
	#	print(d[...])
	#else:
	#	print(d)

	assert( len(d)==15 )

	x = XXX()
	e = x.v[ len(b) : ]
	assert( len(e)==5 )

	f = x.method( x.v[len(b):] )
	assert( len(f)==5 )

main()
```
output:
------
```javascript


var XXX =  function XXX()
{
/***/ if (XXX.__recompile !== undefined) { eval("XXX.__redef="+XXX.__recompile); XXX.__recompile=undefined; };
/***/ if (XXX.__redef !== undefined) { return XXX.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
	/***/ try {
	this.__init__();
	/***/ } catch (__err) { if (__debugger__.onerror(__err, XXX, this.__init__)==true){debugger;}else{throw __err;} };
}/*end->	`XXX`	*/
XXX.locals={};

XXX.prototype.__class__ = XXX;
XXX.__name__ = "XXX";
XXX.__bases__ = [];
XXX.prototype.toString =  function XXX_toString()
{
/***/ if (XXX_toString.__recompile !== undefined) { eval("XXX_toString.__redef="+XXX_toString.__recompile); XXX_toString.__recompile=undefined; };
/***/ if (XXX_toString.__redef !== undefined) { return XXX_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/
XXX.prototype.toString.locals = {};

XXX.prototype.__init__ =  function XXX___init__()
{
/***/ if (XXX___init__.__recompile !== undefined) { eval("XXX___init__.__redef="+XXX___init__.__recompile); XXX___init__.__recompile=undefined; };
/***/ if (XXX___init__.__redef !== undefined) { return XXX___init__.__redef.apply(this,arguments); };
	
	this.v = range(10);
}/*end->	`__init__`	*/
XXX.prototype.__init__.locals = {};

XXX.__init__ = function () { return XXX.prototype.__init__.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
XXX.prototype.method =  function XXX_method(a)
{
/***/ if (XXX_method.__recompile !== undefined) { eval("XXX_method.__redef="+XXX_method.__recompile); XXX_method.__recompile=undefined; };
/***/ if (XXX_method.__redef !== undefined) { return XXX_method.__redef.apply(this,arguments); };
	
	return a;
}/*end->	`method`	*/
XXX.prototype.method.locals = {};

XXX.method = function () { return XXX.prototype.method.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b,e,d,f,x;
	arguments.callee.locals.a=a = range(10).__getslice__(undefined, -5, undefined);
	if (!(len(a) === 5)) {throw new Error("assertion failed"); }
	if (!(a[4] === 4)) {throw new Error("assertion failed"); }
	console.log("--------");
	arguments.callee.locals.b=b = range(10).__getslice_lowerstep__(undefined, 2);
	console.log(b);
	if (!(len(b) === 5)) {throw new Error("assertion failed"); }
	if (!(b[0] === 0)) {throw new Error("assertion failed"); }
	if (!(b[1] === 2)) {throw new Error("assertion failed"); }
	if (!(b[2] === 4)) {throw new Error("assertion failed"); }
	if (!(b[3] === 6)) {throw new Error("assertion failed"); }
	if (!(b[4] === 8)) {throw new Error("assertion failed"); }
	arguments.callee.locals.c=c = range(20);
	arguments.callee.locals.d=d = c.__getslice__(len(b), undefined, undefined);
	if (!(len(d) === 15)) {throw new Error("assertion failed"); }
	arguments.callee.locals.x=x =  new XXX();
	arguments.callee.locals.e=e = x.v.__getslice__(len(b), undefined, undefined);
	if (!(len(e) === 5)) {throw new Error("assertion failed"); }
	arguments.callee.locals.f=f = x.method(x.v.__getslice__(len(b), undefined, undefined));
	if (!(len(f) === 5)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [remove.py](list/remove.py)

input:
------
```python
from runtime import *
"""remove"""

def main():
	a = [1,2]
	a.remove(1)
	assert( len(a) == 1 )


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
	arguments.callee.locals.a=a = [1, 2];
	/***/ try {
	a.remove(1);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, a.remove)==true){debugger;}else{throw __err;} };
	if (!(len(a) === 1)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [neg_index.py](list/neg_index.py)

input:
------
```python
from runtime import *
"""negative list indices"""
def main():
	a = [1,2,3,4]
	## negative indices are allowed when using a number literal as the index,
	## this is the most common use case, because often you want to index from
	## the end with a literal number and not a variable.
	assert( a[-1]==4 )
	assert a[-2]==3
	assert a[-3]==2
	assert a[-4]==1

	## this is allowed in regular python, but not in rusthon.
	idx = -2
	#assert( a[idx]==3 )
	## if you really need to use a variable to perform a negative index,
	## this is the workaround.
	assert a[a.length+idx-1]

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,idx;
	arguments.callee.locals.a=a = [1, 2, 3, 4];
	if (!(a[(a.length + -1)] === 4)) {throw new Error("assertion failed"); }
	if (!(a[(a.length + -2)] === 3)) {throw new Error("assertion failed"); }
	if (!(a[(a.length + -3)] === 2)) {throw new Error("assertion failed"); }
	if (!(a[(a.length + -4)] === 1)) {throw new Error("assertion failed"); }
	arguments.callee.locals.idx=idx = -2;
	if (!(a[((a.length + idx) - 1)])) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [slice_reverse.py](list/slice_reverse.py)

input:
------
```python
from runtime import *
"""list reverse slice"""


def main():
	a = range(10)
	b = a[ 4::-1 ]

	#if BACKEND=='DART':
	#	print(b[...])
	#else:
	#	print(b)


	assert( b[0]==4 )
	assert( b[1]==3 )
	assert( b[2]==2 )
	assert( b[3]==1 )
	assert( b[4]==0 )

	c = range(20)
	d = c[ 2::-1 ]

	#if BACKEND=='DART':
	#	print(d[...])
	#else:
	#	print(d)

	assert( d[0]==2 )
	assert( d[1]==1 )
	assert( d[2]==0 )

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b,d;
	arguments.callee.locals.a=a = range(10);
	arguments.callee.locals.b=b = a.__getslice_lowerstep__(4, -1);
	if (!(b[0] === 4)) {throw new Error("assertion failed"); }
	if (!(b[1] === 3)) {throw new Error("assertion failed"); }
	if (!(b[2] === 2)) {throw new Error("assertion failed"); }
	if (!(b[3] === 1)) {throw new Error("assertion failed"); }
	if (!(b[4] === 0)) {throw new Error("assertion failed"); }
	arguments.callee.locals.c=c = range(20);
	arguments.callee.locals.d=d = c.__getslice_lowerstep__(2, -1);
	if (!(d[0] === 2)) {throw new Error("assertion failed"); }
	if (!(d[1] === 1)) {throw new Error("assertion failed"); }
	if (!(d[2] === 0)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [if_empty.py](list/if_empty.py)

input:
------
```python
from runtime import *
"""if empty list then false"""

class A:
	pass

def main():
	d = []
	#if d:  ## this is not allowed, and will raise an error at runtime
	if len(d):
		err1 = 1
	else:
		err1 = 0

	if len([]):
		err2 = 1
	else:
		err2 = 0

	d.append('xxx')
	if len(d):
		err3 = 0
	else:
		err3 = 1

	assert( err1 == 0 )
	assert( err2 == 0 )
	assert( err3 == 0 )

	a = A()
	ok = False
	#if a:  ## this is not allowed, and will raise an error at runtime
	if a is not None:
		ok = True
	assert ok

	a.x = []
	if len(a.x):
		err4 = 1
	else:
		err4 = 0

	assert( err4 == 0 )

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
A.locals={};

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
/***/ if (A_toString.__recompile !== undefined) { eval("A_toString.__redef="+A_toString.__recompile); A_toString.__recompile=undefined; };
/***/ if (A_toString.__redef !== undefined) { return A_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/
A.prototype.toString.locals = {};

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,ok,d,err3,err2,err1,err4;
	arguments.callee.locals.d=d = [];
	if (len(d) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (len(d))
	{
		arguments.callee.locals.err1=err1 = 1;
	}
	else
	{
		arguments.callee.locals.err1=err1 = 0;
	}
	if (len([]) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (len([]))
	{
		arguments.callee.locals.err2=err2 = 1;
	}
	else
	{
		arguments.callee.locals.err2=err2 = 0;
	}
	/***/ try {
	d.append("xxx");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, d.append)==true){debugger;}else{throw __err;} };
	if (len(d) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (len(d))
	{
		arguments.callee.locals.err3=err3 = 0;
	}
	else
	{
		arguments.callee.locals.err3=err3 = 1;
	}
	if (!(err1 === 0)) {throw new Error("assertion failed"); }
	if (!(err2 === 0)) {throw new Error("assertion failed"); }
	if (!(err3 === 0)) {throw new Error("assertion failed"); }
	arguments.callee.locals.a=a =  new A();
	arguments.callee.locals.ok=ok = false;
		if (a !== null)
	{
		arguments.callee.locals.ok=ok = true;
	}
	if (!(ok)) {throw new Error("assertion failed"); }
	a.x = [];
	if (len(a.x) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (len(a.x))
	{
		arguments.callee.locals.err4=err4 = 1;
	}
	else
	{
		arguments.callee.locals.err4=err4 = 0;
	}
	if (!(err4 === 0)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [insert.py](list/insert.py)

input:
------
```python
from runtime import *
"""insert"""
def main():
	global a
	print 'testing array.insert'
	print []
	print '----'
	a = [1,2,3,4]
	print a.length
	print Object.keys(a)
	print '____'
	print a
	assert( len(a)==4 )

	a.insert(0, 'hi')
	#print a
	assert( len(a)==5 )
	assert( a[0]=='hi' )

	a.insert(1, a.pop(0))
	#print a
	assert( a[0]==1 )
	assert( a[1]=='hi' )

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	
	console.log("testing array.insert");
	console.log([]);
	console.log("----");
	arguments.callee.locals.a=a = [1, 2, 3, 4];
	console.log(a.length);
	console.log(Object.keys(a));
	console.log("____");
	console.log(a);
	if (!(len(a) === 4)) {throw new Error("assertion failed"); }
	/***/ try {
	a.insert(0, "hi");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, a.insert)==true){debugger;}else{throw __err;} };
	if (!(len(a) === 5)) {throw new Error("assertion failed"); }
	if (!(a[0] === "hi")) {throw new Error("assertion failed"); }
	/***/ try {
	a.insert(1, (a instanceof Array ? a.shift() : __jsdict_pop(a, 0)));
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, a.insert)==true){debugger;}else{throw __err;} };
	if (!(a[0] === 1)) {throw new Error("assertion failed"); }
	if (!(a[1] === "hi")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [mul.py](list/mul.py)

input:
------
```python
from runtime import *
"""list multiplication"""


def main():
	a = ['hi']
	print a
	with operator_overloading:
		b = a * 2
	print b
	assert( len(b)==2 )
	assert( b[0]=='hi' )
	assert( b[1]=='hi' )
	print 'ok'

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
	arguments.callee.locals.a=a = ["hi"];
	console.log(a);
	arguments.callee.locals.b=b = (a.__mul__(2));
	console.log(b);
	if (!(len(b) === 2)) {throw new Error("assertion failed"); }
	if (!(b[0] === "hi")) {throw new Error("assertion failed"); }
	if (!(b[1] === "hi")) {throw new Error("assertion failed"); }
	console.log("ok");
}/*end->	`main`	*/
main.locals={};

main();
```
* [set_slice.py](list/set_slice.py)

input:
------
```python
from runtime import *
"""list slice set"""


def main():
	a = list(range(10))
	for v in a: print v
	a[ 2:4 ] = 'Y'
	print a
	print '------------'
	for v in a:
		print v

	assert( a[0]==0 )
	assert( a[1]==1 )

	assert( a[2]=='Y' )

	assert( a[3]==4 )
	assert( a[4]==5 )
	assert( a[5]==6 )
	assert( a[6]==7 )
	assert( a[7]==8 )
	assert( a[8]==9 )

	b = list(range(3))
	print b
	c = b [ :2 ]
	print c
	assert len(c)==2
	assert( c[0]==0 )
	assert( c[1]==1 )
	print '----------'
	print b
	b[ :2 ] = 'ABC'
	print b
	assert( len(b)==4 )
	assert( b[0]=='A' )
	assert( b[1]=='B' )
	assert( b[2]=='C' )
	assert b[3]==2

	e = range(5)
	print e
	e[ 2:3 ] = 'x'
	print e
	assert e[2]=='x'


	d = list(range(10))
	d[ 2:4 ] = [99, 100]
	assert( d[0]==0 )
	assert( d[1]==1 )
	assert( d[2]==99 )
	assert( d[3]==100 )
	print d

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b,e,d;
	arguments.callee.locals.a=a = list(range(10));
	var __iter0 = a;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var v = __iter0[ __n0 ];
		console.log(v);
	}
	/***/ try {
	a.__setslice__(2, 4, undefined, "Y");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, a.__setslice__)==true){debugger;}else{throw __err;} };
	console.log(a);
	console.log("------------");
	var __iter0 = a;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var v = __iter0[ __n0 ];
		console.log(v);
	}
	if (!(a[0] === 0)) {throw new Error("assertion failed"); }
	if (!(a[1] === 1)) {throw new Error("assertion failed"); }
	if (!(a[2] === "Y")) {throw new Error("assertion failed"); }
	if (!(a[3] === 4)) {throw new Error("assertion failed"); }
	if (!(a[4] === 5)) {throw new Error("assertion failed"); }
	if (!(a[5] === 6)) {throw new Error("assertion failed"); }
	if (!(a[6] === 7)) {throw new Error("assertion failed"); }
	if (!(a[7] === 8)) {throw new Error("assertion failed"); }
	if (!(a[8] === 9)) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = list(range(3));
	console.log(b);
	arguments.callee.locals.c=c = b.__getslice__(undefined, 2, undefined);
	console.log(c);
	if (!(len(c) === 2)) {throw new Error("assertion failed"); }
	if (!(c[0] === 0)) {throw new Error("assertion failed"); }
	if (!(c[1] === 1)) {throw new Error("assertion failed"); }
	console.log("----------");
	console.log(b);
	/***/ try {
	b.__setslice__(undefined, 2, undefined, "ABC");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, b.__setslice__)==true){debugger;}else{throw __err;} };
	console.log(b);
	if (!(len(b) === 4)) {throw new Error("assertion failed"); }
	if (!(b[0] === "A")) {throw new Error("assertion failed"); }
	if (!(b[1] === "B")) {throw new Error("assertion failed"); }
	if (!(b[2] === "C")) {throw new Error("assertion failed"); }
	if (!(b[3] === 2)) {throw new Error("assertion failed"); }
	arguments.callee.locals.e=e = range(5);
	console.log(e);
	/***/ try {
	e.__setslice__(2, 3, undefined, "x");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, e.__setslice__)==true){debugger;}else{throw __err;} };
	console.log(e);
	if (!(e[2] === "x")) {throw new Error("assertion failed"); }
	arguments.callee.locals.d=d = list(range(10));
	/***/ try {
	d.__setslice__(2, 4, undefined, [99, 100]);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, d.__setslice__)==true){debugger;}else{throw __err;} };
	if (!(d[0] === 0)) {throw new Error("assertion failed"); }
	if (!(d[1] === 1)) {throw new Error("assertion failed"); }
	if (!(d[2] === 99)) {throw new Error("assertion failed"); }
	if (!(d[3] === 100)) {throw new Error("assertion failed"); }
	console.log(d);
}/*end->	`main`	*/
main.locals={};

main();
```
* [index.py](list/index.py)

input:
------
```python
from runtime import *
"""list indices"""
def main():
	a = [1,2,3,4]
	idx = 1
	assert( a[0]==1 )
	assert( a[idx]==2 )
	assert( a.index(3)==2 )

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,idx;
	arguments.callee.locals.a=a = [1, 2, 3, 4];
	arguments.callee.locals.idx=idx = 1;
	if (!(a[0] === 1)) {throw new Error("assertion failed"); }
	if (!(a[idx] === 2)) {throw new Error("assertion failed"); }
	if (!(a.index(3) === 2)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [loop.py](list/loop.py)

input:
------
```python
from runtime import *
'''
simple for loop
'''

def main():
	a = [1,2,3]
	y = 0
	for x in a:
		y += x
	assert( y==6 )

	b = range(3)
	z = 0
	for x in b:
		z += x
	assert( z==3 )

	w = 0
	for i in a:
		for j in b:
			w += 1
	assert( w==9 )

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,y,b,z,w;
	arguments.callee.locals.a=a = [1, 2, 3];
	arguments.callee.locals.y=y = 0;
	var __iter0 = a;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var x = __iter0[ __n0 ];
		if (y instanceof Array || __is_typed_array(y)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { y += x; }
	}
	if (!(y === 6)) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = range(3);
	arguments.callee.locals.z=z = 0;
	var __iter0 = b;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var x = __iter0[ __n0 ];
		if (z instanceof Array || __is_typed_array(z)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { z += x; }
	}
	if (!(z === 3)) {throw new Error("assertion failed"); }
	arguments.callee.locals.w=w = 0;
	var __iter0 = a;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var i = __iter0[ __n0 ];
		var __iter1 = b;
		if (! (__iter1 instanceof Array || typeof __iter1 == "string" || __is_typed_array(__iter1) || __is_some_array(__iter1) )) { __iter1 = __object_keys__(__iter1) }
		for (var __n1 = 0; __n1 < __iter1.length; __n1++) {
			var j = __iter1[ __n1 ];
			w ++;
		}
	}
	if (!(w === 9)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [setitem.py](list/setitem.py)

input:
------
```python
from runtime import *
"""setitem and append"""
def main():
	a = [1,2,3,4]
	idx = 1
	assert( a[0]==1 )
	assert( a[idx]==2 )

	a[ 0 ] = 'hello'
	a[ 1 ] = 'world'
	assert( a[0]=='hello' )
	assert( a[1]=='world' )

	a.append( 'xxx' )
	assert( a[4]=='xxx' )
	assert( len(a)==5 )

	a.append( 'yyy' )
	assert( a[5]=='yyy' )
	assert( len(a)==6 )

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,idx;
	arguments.callee.locals.a=a = [1, 2, 3, 4];
	arguments.callee.locals.idx=idx = 1;
	if (!(a[0] === 1)) {throw new Error("assertion failed"); }
	if (!(a[idx] === 2)) {throw new Error("assertion failed"); }
	if (a.__setitem__) { a.__setitem__(0, "hello") }
	else { a[0] = "hello" }
	if (a.__setitem__) { a.__setitem__(1, "world") }
	else { a[1] = "world" }
	if (!(a[0] === "hello")) {throw new Error("assertion failed"); }
	if (!(a[1] === "world")) {throw new Error("assertion failed"); }
	/***/ try {
	a.append("xxx");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, a.append)==true){debugger;}else{throw __err;} };
	if (!(a[4] === "xxx")) {throw new Error("assertion failed"); }
	if (!(len(a) === 5)) {throw new Error("assertion failed"); }
	/***/ try {
	a.append("yyy");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, a.append)==true){debugger;}else{throw __err;} };
	if (!(a[5] === "yyy")) {throw new Error("assertion failed"); }
	if (!(len(a) === 6)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [sort.py](list/sort.py)

input:
------
```python
from runtime import *
"""list sort"""

def main():
	x = [100, 10, 3,2,1]
	x.sort()
	assert( x[0]==1 )
	assert( x[1]==2 )
	assert( x[2]==3 )
	assert( x[3]==10 )
	assert( x[4]==100 )

	y = ['C', 'B', 'A']
	y.sort()
	assert( y[0]=='A' )
	assert( y[1]=='B' )
	assert( y[2]=='C' )

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var y,x;
	arguments.callee.locals.x=x = [100, 10, 3, 2, 1];
	/***/ try {
	__sort_method(x);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, __sort_method)==true){debugger;}else{throw __err;} };
	if (!(x[0] === 1)) {throw new Error("assertion failed"); }
	if (!(x[1] === 2)) {throw new Error("assertion failed"); }
	if (!(x[2] === 3)) {throw new Error("assertion failed"); }
	if (!(x[3] === 10)) {throw new Error("assertion failed"); }
	if (!(x[4] === 100)) {throw new Error("assertion failed"); }
	arguments.callee.locals.y=y = ["C", "B", "A"];
	/***/ try {
	__sort_method(y);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, __sort_method)==true){debugger;}else{throw __err;} };
	if (!(y[0] === "A")) {throw new Error("assertion failed"); }
	if (!(y[1] === "B")) {throw new Error("assertion failed"); }
	if (!(y[2] === "C")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [contains.py](list/contains.py)

input:
------
```python
from runtime import *
"""if x in list"""
def main():
	a = ['foo', 'bar']
	assert( 'foo' in a )

	b = [0, 1, 2]
	assert( 2 in b )

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
	arguments.callee.locals.a=a = ["foo", "bar"];
	if (!(__contains__(a, "foo"))) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = [0, 1, 2];
	if (!(__contains__(b, 2))) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [pop.py](list/pop.py)

input:
------
```python
from runtime import *
"""list.pop(n)"""


def main():
	a = list(range(10))
	print a
	b = a.pop()
	print b
	print a
	assert( b==9 )
	c = a.pop(0)
	assert( c==0 )

	d = ['A', 'B', 'C']
	assert( d.pop(1)=='B' )
	assert( len(d)==2 )
main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b,d;
	arguments.callee.locals.a=a = list(range(10));
	console.log(a);
	arguments.callee.locals.b=b = a.pop();
	console.log(b);
	console.log(a);
	if (!(b === 9)) {throw new Error("assertion failed"); }
	arguments.callee.locals.c=c = (a instanceof Array ? a.shift() : __jsdict_pop(a, 0));
	if (!(c === 0)) {throw new Error("assertion failed"); }
	arguments.callee.locals.d=d = ["A", "B", "C"];
	if (!(__jsdict_pop(d, 1) === "B")) {throw new Error("assertion failed"); }
	if (!(len(d) === 2)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```
* [comp.py](list/comp.py)

input:
------
```python
from runtime import *
'''
list comprehensions
'''

def main():
	a = [x for x in range(3)]
	assert( len(a)==3 )
	assert( a[0]==0 )
	assert( a[1]==1 )
	assert( a[2]==2 )

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
	var __comp__0;
	var idx0;
	var iter0;
	var get0;
	arguments.callee.locals.__comp__0=__comp__0 = [];
	arguments.callee.locals.idx0=idx0 = 0;
	arguments.callee.locals.iter0=iter0 = 3;
	while (idx0 < iter0)
	{
		var x;
		arguments.callee.locals.x=x = idx0;
		/***/ try {
		__comp__0.push(x);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, __comp__0.push)==true){debugger;}else{throw __err;} };
		idx0 ++;
	}
	arguments.callee.locals.a=a = __comp__0;
	if (!(len(a) === 3)) {throw new Error("assertion failed"); }
	if (!(a[0] === 0)) {throw new Error("assertion failed"); }
	if (!(a[1] === 1)) {throw new Error("assertion failed"); }
	if (!(a[2] === 2)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```