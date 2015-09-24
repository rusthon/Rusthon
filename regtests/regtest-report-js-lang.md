JavaScript Backend Regression Tests - lang
-----------------------------
the following tests compiled, and run in nodejs without any errors
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
/***/ if (f.__recompile !== undefined) { eval("f.__redef="+f.__recompile); f.__recompile=undefined; };
/***/ if (f.__redef !== undefined) { return f.__redef.apply(this,arguments); };
	var l;
/***/ if (!(isinstance(l,Array))) {throw new TypeError("invalid type - not an array")};
/***/ if (l.length > 0 && !( isinstance(l[0], int) )) {throw new TypeError("invalid array type")};
	/***/ try {
	l.append(1);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, f, l.append)==true){debugger;}else{throw __err;} };
}/*end->	`f`	*/
f.args = ["[]int"];

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,b;
	a = [1,2,3] /*array of: int*/;
	if (!(a[0] === 1)) {throw new Error("assertion failed"); }
	/***/ try {
	f(a);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, f)==true){debugger;}else{throw __err;} };
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
		/***/ try {
		__comp__0.push(x);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, __comp__0.push)==true){debugger;}else{throw __err;} };
		idx0 ++;
	}
	b = __comp__0;
	/***/ try {
	f(b);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, f)==true){debugger;}else{throw __err;} };
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
/***/ if (f.__recompile !== undefined) { eval("f.__redef="+f.__recompile); f.__recompile=undefined; };
/***/ if (f.__redef !== undefined) { return f.__redef.apply(this,arguments); };
	var m;
/***/ if (m.__keytype__ != "string") {throw new TypeError("invalid dict key type")};
/***/ if (m.__valuetype__ != "int") {throw new TypeError("invalid dict value type")};
	if (m.__setitem__) { m.__setitem__("x", 100) }
	else { m["x"] = 100 }
}/*end->	`f`	*/
f.args = ["map[string]int"];

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a;
	a = dict({  }, { copy:false, keytype:"string", iterable:[["x", 1], ["y", 2], ["z", 3]] ,valuetype:"int" });
	if (!(a["x"] === 1)) {throw new Error("assertion failed"); }
	/***/ try {
	f(a);
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, f)==true){debugger;}else{throw __err;} };
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
var __$UID$__=0;
var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	
	/***/ try {
	now = new Date();
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, JS)==true){debugger;}else{throw __err;} };
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,b;
	a = false;
	b = false;
	if (! (a) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (! (a))
	{
		b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	a = 0;
	b = false;
	if (! (a) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (! (a))
	{
		b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	a = 0.0;
	b = false;
	if (! (a) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (! (a))
	{
		b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	a = null;
	b = false;
	if (! (a) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
/***/ if (foo.__recompile !== undefined) { eval("foo.__redef="+foo.__recompile); foo.__recompile=undefined; };
/***/ if (foo.__redef !== undefined) { return foo.__redef.apply(this,arguments); };
	
	return 42;
}/*end->	`foo`	*/

var __lambda__ =  function __lambda__()
{
/***/ if (__lambda__.__recompile !== undefined) { eval("__lambda__.__redef="+__lambda__.__recompile); __lambda__.__recompile=undefined; };
/***/ if (__lambda__.__redef !== undefined) { return __lambda__.__redef.apply(this,arguments); };
	
	return 42;
}/*end->	`__lambda__`	*/

bar = __lambda__;
var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	
	/***/ try {
	eval("a = bar()");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, eval)==true){debugger;}else{throw __err;} };
	/***/ try {
	eval("b = foo()");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, eval)==true){debugger;}else{throw __err;} };
	if (!(a === 42)) {throw new Error("assertion failed"); }
	if (!(b === 42)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [typedarrays.py](lang/typedarrays.py)

input:
------
```python
from runtime import *
'''
javascript typed array syntax
'''

def main():
	s = [10,20,30]
	for v in s:
		print v
	print s

	print 'testing javascript typed arrays'
	a = [128]int( 1,2,3 )
	print __is_some_array(a)

	assert len(a)==128
	assert isinstance(a, Int32Array)
	assert a[0]==1
	assert a[1]==2
	assert a[2]==3
	assert a[3]==0

	ii = 0
	#for value in a:  ## will raise a runtime error
	for value in iter(a):
		print value
		ii += 1
		if ii > 10: break
	#print a

	b = [128]int32(1,2,3)
	c = [128]i32(1,2,3)
	assert isinstance(b, Int32Array)
	assert isinstance(c, Int32Array)

	d = [128]float( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float32Array)
	d = [128]float32( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float32Array)
	d = [128]f32( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float32Array)

	d = [128]float64( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float64Array)
	d = [128]f64( 1.1, 2.2, 3.3 )
	assert isinstance(d, Float64Array)
	print d[0]
	print d[1]
	print d[2]


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
	var a,c,b,d,ii,s;
	s = [10, 20, 30];
	var __iter0 = s;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var v = __iter0[ __n0 ];
		console.log(v);
	}
	console.log(s);
	console.log("testing javascript typed arrays");
	a = __array_fill__( new Int32Array(128), [1,2,3]);
	console.log(__is_some_array(a));
	if (!(len(a) === 128)) {throw new Error("assertion failed"); }
	if (!(isinstance(a, Int32Array))) {throw new Error("assertion failed"); }
	if (!(a[0] === 1)) {throw new Error("assertion failed"); }
	if (!(a[1] === 2)) {throw new Error("assertion failed"); }
	if (!(a[2] === 3)) {throw new Error("assertion failed"); }
	if (!(a[3] === 0)) {throw new Error("assertion failed"); }
	ii = 0;
	var __iter0 = a;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var value = __iter0[ __n0 ];
		console.log(value);
		ii ++;
				if (ii > 10)
		{
			break;
		}
	}
	b = __array_fill__( new Int32Array(128), [1,2,3]);
	c = __array_fill__( new Int32Array(128), [1,2,3]);
	if (!(isinstance(b, Int32Array))) {throw new Error("assertion failed"); }
	if (!(isinstance(c, Int32Array))) {throw new Error("assertion failed"); }
	d = __array_fill__( new Float32Array(128), [1.1,2.2,3.3]);
	if (!(isinstance(d, Float32Array))) {throw new Error("assertion failed"); }
	d = __array_fill__( new Float32Array(128), [1.1,2.2,3.3]);
	if (!(isinstance(d, Float32Array))) {throw new Error("assertion failed"); }
	d = __array_fill__( new Float32Array(128), [1.1,2.2,3.3]);
	if (!(isinstance(d, Float32Array))) {throw new Error("assertion failed"); }
	d = __array_fill__( new Float64Array(128), [1.1,2.2,3.3]);
	if (!(isinstance(d, Float64Array))) {throw new Error("assertion failed"); }
	d = __array_fill__( new Float64Array(128), [1.1,2.2,3.3]);
	if (!(isinstance(d, Float64Array))) {throw new Error("assertion failed"); }
	console.log(d[0]);
	console.log(d[1]);
	console.log(d[2]);
	console.log("ok");
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
def func(x=False, callback=None ):
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

	def cb() ->int:
		return 1+1

	func( callback=cb )



main()
```
output:
------
```javascript


var func =  function func(_kwargs_)
{
/***/ if (func.__recompile !== undefined) { eval("func.__redef="+func.__recompile); func.__recompile=undefined; };
/***/ if (func.__redef !== undefined) { return func.__redef.apply(this,arguments); };
	var a;
	var x        = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.x===undefined))       ?	false :   typeof(_kwargs_)=='object'?_kwargs_.x: __invalid_call__('function `func` requires named keyword arguments, invalid parameter for `x`',arguments);
	var callback = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.callback===undefined))?	null  :   typeof(_kwargs_)=='object'?_kwargs_.callback: __invalid_call__('function `func` requires named keyword arguments, invalid parameter for `callback`',arguments);
	a = false;
	if (x instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
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
	if (callback instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a;
	a = false;
	if (1 instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (1)
	{
		a = true;
	}
	if (!(a === true)) {throw new Error("assertion failed"); }
	a = false;
	if (false instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
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
	if (null instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (null)
	{
		a = false;
	}
	else
	{
		a = true;
	}
	if (!(a === true)) {throw new Error("assertion failed"); }
			var cb =  function cb()
	{
/***/ if (cb.__recompile !== undefined) { eval("cb.__redef="+cb.__recompile); cb.__recompile=undefined; };
/***/ if (cb.__redef !== undefined) { return cb.__redef.apply(this,arguments); };
		
		return (1 + 1);
	}/*end->	`cb`	*/
cb.returns = "int";

	/***/ try {
	func({ callback:cb });
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, func)==true){debugger;}else{throw __err;} };
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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