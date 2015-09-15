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
		y += x;
	}
	if (!(y === 6)) {throw new Error("assertion failed"); }
	z = "";
	arr = ["a", "b", "c"];
	var __iter0 = arr;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var v = __iter0[ __n0 ];
		z += v;
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
		z += char;
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
		k += key;
		v += ob[key];
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