JavaScript Backend Regression Tests - calling
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
/***/ if (f1.__recompile !== undefined) { eval("f1.__redef="+f1.__recompile); f1.__recompile=undefined; };
/***/ if (f1.__redef !== undefined) { return f1.__redef.apply(this,arguments); };
	
	return a;
}/*end->	`f1`	*/

var f2 =  function f2(_kwargs_)
{
/***/ if (f2.__recompile !== undefined) { eval("f2.__redef="+f2.__recompile); f2.__recompile=undefined; };
/***/ if (f2.__redef !== undefined) { return f2.__redef.apply(this,arguments); };
	
	var a = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.a===undefined))?	1 :   typeof(_kwargs_)=='object'?_kwargs_.a: __invalid_call__('function `f2` requires named keyword arguments, invalid parameter for `a`',arguments);
	var b = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.b===undefined))?	2 :   typeof(_kwargs_)=='object'?_kwargs_.b: __invalid_call__('function `f2` requires named keyword arguments, invalid parameter for `b`',arguments);
	return (a + b);
}/*end->	`f2`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	
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
		for key in kw.keys():
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

A.prototype.f2 =  function A_f2(kw)
{
/***/ if (A_f2.__recompile !== undefined) { eval("A_f2.__redef="+A_f2.__recompile); A_f2.__recompile=undefined; };
/***/ if (A_f2.__redef !== undefined) { return A_f2.__redef.apply(this,arguments); };
	var a;
	a = 0;
	var __iter0 = __jsdict_keys(kw);
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var key = __iter0[ __n0 ];
		if (a instanceof Array || __is_typed_array(a)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { a += kw[key]; }
	}
	return a;
}/*end->	`f2`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
		for key in iter(kw):
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
/***/ if (A.__recompile !== undefined) { eval("A.__redef="+A.__recompile); A.__recompile=undefined; };
/***/ if (A.__redef !== undefined) { return A.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
	/***/ try {
	this.__init__(kw);
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

A.prototype.__init__ =  function A___init__(kw)
{
/***/ if (A___init__.__recompile !== undefined) { eval("A___init__.__redef="+A___init__.__recompile); A___init__.__recompile=undefined; };
/***/ if (A___init__.__redef !== undefined) { return A___init__.__redef.apply(this,arguments); };
	var a;
	a = 0;
	var __iter0 = kw;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var key = __iter0[ __n0 ];
		if (a instanceof Array || __is_typed_array(a)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { a += kw[key]; }
	}
	this.value = a;
}/*end->	`__init__`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
/***/ if (get_lambda.__recompile !== undefined) { eval("get_lambda.__redef="+get_lambda.__recompile); get_lambda.__recompile=undefined; };
/***/ if (get_lambda.__redef !== undefined) { return get_lambda.__redef.apply(this,arguments); };
	
			var __lambda__ =  function __lambda__(x, y)
	{
/***/ if (__lambda__.__recompile !== undefined) { eval("__lambda__.__redef="+__lambda__.__recompile); __lambda__.__recompile=undefined; };
/***/ if (__lambda__.__redef !== undefined) { return __lambda__.__redef.apply(this,arguments); };
		
		return (x + y);
	}/*end->	`__lambda__`	*/

	return __lambda__;
}/*end->	`get_lambda`	*/

var get_lambdas =  function get_lambdas()
{
/***/ if (get_lambdas.__recompile !== undefined) { eval("get_lambdas.__redef="+get_lambdas.__recompile); get_lambdas.__recompile=undefined; };
/***/ if (get_lambdas.__redef !== undefined) { return get_lambdas.__redef.apply(this,arguments); };
	
	return [(function (a,b) {return (a + b);}), (function (x,y) {return (x + y);})];
}/*end->	`get_lambdas`	*/

var call_lambda =  function call_lambda(F)
{
/***/ if (call_lambda.__recompile !== undefined) { eval("call_lambda.__redef="+call_lambda.__recompile); call_lambda.__recompile=undefined; };
/***/ if (call_lambda.__redef !== undefined) { return call_lambda.__redef.apply(this,arguments); };
	
	return F();
}/*end->	`call_lambda`	*/

var call_lambda2 =  function call_lambda2(_kwargs_)
{
/***/ if (call_lambda2.__recompile !== undefined) { eval("call_lambda2.__redef="+call_lambda2.__recompile); call_lambda2.__recompile=undefined; };
/***/ if (call_lambda2.__redef !== undefined) { return call_lambda2.__redef.apply(this,arguments); };
	
	var callback = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.callback===undefined))?	null :   typeof(_kwargs_)=='object'?_kwargs_.callback: __invalid_call__('function `call_lambda2` requires named keyword arguments, invalid parameter for `callback`',arguments);
	return callback();
}/*end->	`call_lambda2`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var funcs,r,e,d,f;
			var __lambda__ =  function __lambda__(a, b)
	{
/***/ if (__lambda__.__recompile !== undefined) { eval("__lambda__.__redef="+__lambda__.__recompile); __lambda__.__recompile=undefined; };
/***/ if (__lambda__.__redef !== undefined) { return __lambda__.__redef.apply(this,arguments); };
		
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
	for key in iter(kw):
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
/***/ if (f2.__recompile !== undefined) { eval("f2.__redef="+f2.__recompile); f2.__recompile=undefined; };
/***/ if (f2.__redef !== undefined) { return f2.__redef.apply(this,arguments); };
	var a;
	a = 0;
	var __iter0 = kw;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var key = __iter0[ __n0 ];
		if (a instanceof Array || __is_typed_array(a)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { a += kw[key]; }
	}
	return a;
}/*end->	`f2`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	
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
/***/ if (f.__recompile !== undefined) { eval("f.__redef="+f.__recompile); f.__recompile=undefined; };
/***/ if (f.__redef !== undefined) { return f.__redef.apply(this,arguments); };
var args = Array.prototype.splice.call(arguments,1, arguments.length);
	var c;
	console.log("*args");
	console.log(args);
	c = a;
	var __iter0 = args;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var b = __iter0[ __n0 ];
		if (c instanceof Array || __is_typed_array(c)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { c += b; }
	}
	return c;
}/*end->	`f`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	
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
/***/ if (f.__recompile !== undefined) { eval("f.__redef="+f.__recompile); f.__recompile=undefined; };
/***/ if (f.__redef !== undefined) { return f.__redef.apply(this,arguments); };
	
	return ((a + b) + c);
}/*end->	`f`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	
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
/***/ if (f.__recompile !== undefined) { eval("f.__redef="+f.__recompile); f.__recompile=undefined; };
/***/ if (f.__redef !== undefined) { return f.__redef.apply(this,arguments); };
	
	var b = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.b===undefined))?	null :   typeof(_kwargs_)=='object'?_kwargs_.b: __invalid_call__('function `f` requires named keyword arguments, invalid parameter for `b`',arguments);
	var c = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.c===undefined))?	null :   typeof(_kwargs_)=='object'?_kwargs_.c: __invalid_call__('function `f` requires named keyword arguments, invalid parameter for `c`',arguments);
	return ((a + b) * c);
}/*end->	`f`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	
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
/***/ if (f.__recompile !== undefined) { eval("f.__redef="+f.__recompile); f.__recompile=undefined; };
/***/ if (f.__redef !== undefined) { return f.__redef.apply(this,arguments); };
	
	return (((x + a) + b) + c);
}/*end->	`f`	*/

var f2 =  function f2(x, y, z, _kwargs_)
{
/***/ if (f2.__recompile !== undefined) { eval("f2.__redef="+f2.__recompile); f2.__recompile=undefined; };
/***/ if (f2.__redef !== undefined) { return f2.__redef.apply(this,arguments); };
	
	var w = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.w===undefined))?	0 :   typeof(_kwargs_)=='object'?_kwargs_.w: __invalid_call__('function `f2` requires named keyword arguments, invalid parameter for `w`',arguments);
	return (((x + y) + z) + w);
}/*end->	`f2`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,b;
	a = [1, 1, 1];
	if (!(f.apply(f, [].extend([1]).extend(a)) === 4)) {throw new Error("assertion failed"); }
	if (!(f2.apply(f2, [].extend(a).append({ w:10 })) === 13)) {throw new Error("assertion failed"); }
	b = [1, 1];
	if (!(f2.apply(f2, [].extend([100]).extend(b).append({ w:10 })) === 112)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```