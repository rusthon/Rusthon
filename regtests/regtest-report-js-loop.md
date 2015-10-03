JavaScript Backend Regression Tests - loop
-----------------------------
the following tests compiled, and run in nodejs without any errors
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
	for char in iter(s):
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
	for key in iter(ob):
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,arr,b,e,keys,k,ob,s,values,v,y,z,ob2;
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
	arguments.callee.locals.z=z = "";
	arguments.callee.locals.arr=arr = ["a", "b", "c"];
	var __iter0 = arr;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var v = __iter0[ __n0 ];
		if (z instanceof Array || __is_typed_array(z)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { z += v; }
	}
	if (!(z === "abc")) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = false;
	if (__contains__(arr, "a") instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (__contains__(arr, "a"))
	{
		arguments.callee.locals.b=b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	arguments.callee.locals.s=s = "hello world";
	arguments.callee.locals.z=z = "";
	var __iter0 = s;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var char = __iter0[ __n0 ];
		if (z instanceof Array || __is_typed_array(z)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { z += char; }
	}
	if (!(z === "hello world")) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = false;
	if (__contains__(s, "hello") instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (__contains__(s, "hello"))
	{
		arguments.callee.locals.b=b = true;
	}
	if (!(b === true)) {throw new Error("assertion failed"); }
	console.log("testing for loop over dict");
	arguments.callee.locals.ob=ob = dict({  }, { copy:false, keytype:"string", iterable:[["a", "A"], ["b", "B"]] });
	arguments.callee.locals.k=k = "";
	arguments.callee.locals.v=v = "";
	var __iter0 = ob;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var key = __iter0[ __n0 ];
		if (k instanceof Array || __is_typed_array(k)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { k += key; }
		if (v instanceof Array || __is_typed_array(v)) { throw new RuntimeError("Array += Array is not allowed without operator overloading"); }
		else { v += ob[key]; }
	}
	console.log(k);
	console.log(v);
	if (!((k === "ab" || k === "ba"))) {throw new Error("assertion failed"); }
	if (!((v === "AB" || v === "BA"))) {throw new Error("assertion failed"); }
	arguments.callee.locals.keys=keys = [];
	arguments.callee.locals.values=values = [];
	var __mtarget__4,x;
	var __iter0 = __jsdict_items(ob);
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var __mtarget__4 = __iter0[ __n0 ];
		arguments.callee.locals.x=x = __mtarget__4[0];
		arguments.callee.locals.y=y = __mtarget__4[1];
		/***/ try {
		keys.append(x);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, keys.append)==true){debugger;}else{throw __err;} };
		/***/ try {
		values.append(y);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, values.append)==true){debugger;}else{throw __err;} };
	}
	if (!(__contains__(keys, "a"))) {throw new Error("assertion failed"); }
	if (!(__contains__(values, "A"))) {throw new Error("assertion failed"); }
	arguments.callee.locals.ob2=ob2 = dict({  }, { copy:false, keytype:"string", iterable:[["c", "C"], ["d", "D"]] });
	arguments.callee.locals.e=e = 0;
	arguments.callee.locals.arr=arr = [];
	var __mtarget__5;
	var __iter0 = __jsdict_items(ob);
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var __mtarget__5 = __iter0[ __n0 ];
		arguments.callee.locals.x=x = __mtarget__5[0];
		arguments.callee.locals.y=y = __mtarget__5[1];
		/***/ try {
		arr.append(x);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, arr.append)==true){debugger;}else{throw __err;} };
		/***/ try {
		arr.append(y);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, arr.append)==true){debugger;}else{throw __err;} };
		var __mtarget__6,w;
		var __iter1 = __jsdict_items(ob2);
		if (! (__iter1 instanceof Array || typeof __iter1 == "string" || __is_typed_array(__iter1) || __is_some_array(__iter1) )) { __iter1 = __object_keys__(__iter1) }
		for (var __n1 = 0; __n1 < __iter1.length; __n1++) {
			var __mtarget__6 = __iter1[ __n1 ];
			arguments.callee.locals.w=w = __mtarget__6[0];
			arguments.callee.locals.z=z = __mtarget__6[1];
			e ++;
			/***/ try {
			arr.append(w);
			/***/ } catch (__err) { if (__debugger__.onerror(__err, main, arr.append)==true){debugger;}else{throw __err;} };
			/***/ try {
			arr.append(z);
			/***/ } catch (__err) { if (__debugger__.onerror(__err, main, arr.append)==true){debugger;}else{throw __err;} };
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
main.locals={};

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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,c,b,e,d;
	arguments.callee.locals.a=a = range(10);
	if (!(a[0] === 0)) {throw new Error("assertion failed"); }
	if (!(a[1] === 1)) {throw new Error("assertion failed"); }
	if (!(len(a) === 10)) {throw new Error("assertion failed"); }
	arguments.callee.locals.b=b = range(1, 10);
	if (!(b[0] === 1)) {throw new Error("assertion failed"); }
	if (!(b[1] === 2)) {throw new Error("assertion failed"); }
	if (!(len(b) === 9)) {throw new Error("assertion failed"); }
	arguments.callee.locals.c=c = 0;
	/*for var in range*/;
	var i;
	arguments.callee.locals.i=i = -1;
	while (++i < 10)
	{
		c ++;
	}
	if (!(c === 10)) {throw new Error("assertion failed"); }
	arguments.callee.locals.d=d = 0;
	/*for var in range*/;
	
	arguments.callee.locals.i=i = (1 - 1);
	while (++i < 10)
	{
		d ++;
	}
	if (!(d === 9)) {throw new Error("assertion failed"); }
	arguments.callee.locals.e=e = 0;
	/*for var in range*/;
	
	arguments.callee.locals.i=i = (1 - 1);
	var i__end__;
	arguments.callee.locals.i__end__=i__end__ = (8 + 2);
	while (++i < i__end__)
	{
		e ++;
	}
	if (!(e === 9)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,i,j;
	arguments.callee.locals.a=a = 0;
	arguments.callee.locals.i=i = 0;
	while (i < 10)
	{
		arguments.callee.locals.j=j = 0;
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
		/***/ try {
		arr1.append(1);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, arr1.append)==true){debugger;}else{throw __err;} };
		/***/ try {
		arr2.append(2);
		/***/ } catch (__err) { if (__debugger__.onerror(__err, main, arr2.append)==true){debugger;}else{throw __err;} };
	}
	if (!(len(arr1) === 5)) {throw new Error("assertion failed"); }
	if (!(len(arr2) === 5)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/
main.locals={};

main();
```