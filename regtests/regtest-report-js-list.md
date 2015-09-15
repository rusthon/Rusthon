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
	var a,c,b,e,d,n,w;
	a = [1, 2];
	b = [3, 4];
	n = 1;
	w = 100;
	c = (a.__add__(b));
if (n instanceof Array || __is_typed_array(n)) { n.extend(n); }
	else if (n.__iadd__) { n.__iadd__(n); }
	else { n += n; }
w = (w.__add__(w));
	if (!(n === 2)) {throw new Error("assertion failed"); }
	if (!(w === 200)) {throw new Error("assertion failed"); }
	if (!(len(c) === 4)) {throw new Error("assertion failed"); }
	if (!(c[0] === 1)) {throw new Error("assertion failed"); }
	if (!(c[1] === 2)) {throw new Error("assertion failed"); }
	if (!(c[2] === 3)) {throw new Error("assertion failed"); }
	if (!(c[3] === 4)) {throw new Error("assertion failed"); }
	d = a.__add__(b);
	if (!(len(d) === 4)) {throw new Error("assertion failed"); }
	e = a.add(b);
	if (!(len(e) === 4)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var a,b;
	a = range(10);
	if (!(len(a) === 10)) {throw new Error("assertion failed"); }
	if (!(a[0] === 0)) {throw new Error("assertion failed"); }
	if (!(a[9] === 9)) {throw new Error("assertion failed"); }
	b = range(1, 10);
	if (!(len(b) === 9)) {throw new Error("assertion failed"); }
	if (!(b[0] === 1)) {throw new Error("assertion failed"); }
	if (!(b[8] === 9)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var a,b;
	a = [1, 2, 3, 4];
	if (!(len(a) === 4)) {throw new Error("assertion failed"); }
	b = list();
	if (!(len(b) === 0)) {throw new Error("assertion failed"); }
	b.append(5);
	if (!(len(b) === 1)) {throw new Error("assertion failed"); }
	if (a instanceof Array || __is_typed_array(a)) { a.extend(b); }
	else if (a.__iadd__) { a.__iadd__(b); }
	else { a += b; }
	if (!(len(a) === 5)) {throw new Error("assertion failed"); }
	a.extend(b);
	if (!(len(a) === 6)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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

	#if BACKEND=='DART':
	#	print(a[...])
	#else:
	#	print(a)


	b = range(10)[::2]
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
	this.__$UID$__ = __$UID$__ ++;
	this.__init__();
}/*end->	`XXX`	*/

XXX.prototype.__class__ = XXX;
XXX.__name__ = "XXX";
XXX.__bases__ = [];
XXX.prototype.toString =  function XXX_toString()
{
	return this.__$UID$__;
}/*end->	`toString`	*/

XXX.prototype.__init__ =  function XXX___init__()
{
	
	this.v = range(10);
}/*end->	`__init__`	*/

XXX.prototype.method =  function XXX_method(a)
{
	
	return a;
}/*end->	`method`	*/

var main =  function main()
{
	var a,c,b,e,d,f,x;
	a = range(10).__getslice__(undefined, -5, undefined);
	if (!(len(a) === 5)) {throw new Error("assertion failed"); }
	if (!(a[4] === 4)) {throw new Error("assertion failed"); }
	b = range(10).__getslice__(undefined, undefined, 2);
	if (!(len(b) === 5)) {throw new Error("assertion failed"); }
	if (!(b[0] === 0)) {throw new Error("assertion failed"); }
	if (!(b[1] === 2)) {throw new Error("assertion failed"); }
	if (!(b[2] === 4)) {throw new Error("assertion failed"); }
	if (!(b[3] === 6)) {throw new Error("assertion failed"); }
	if (!(b[4] === 8)) {throw new Error("assertion failed"); }
	c = range(20);
	d = c.__getslice__(len(b), undefined, undefined);
	if (!(len(d) === 15)) {throw new Error("assertion failed"); }
	x =  new XXX();
	e = x.v.__getslice__(len(b), undefined, undefined);
	if (!(len(e) === 5)) {throw new Error("assertion failed"); }
	f = x.method(x.v.__getslice__(len(b), undefined, undefined));
	if (!(len(f) === 5)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var a;
	a = [1, 2];
	a.remove(1);
	if (!(len(a) === 1)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var a,idx;
	a = [1, 2, 3, 4];
	if (!(a[(a.length + -1)] === 4)) {throw new Error("assertion failed"); }
	if (!(a[(a.length + -2)] === 3)) {throw new Error("assertion failed"); }
	if (!(a[(a.length + -3)] === 2)) {throw new Error("assertion failed"); }
	if (!(a[(a.length + -4)] === 1)) {throw new Error("assertion failed"); }
	idx = -2;
	if (!(a[((a.length + idx) - 1)])) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var a,c,b,d;
	a = range(10);
	b = a.__getslice__(4, undefined, -1);
	if (!(b[0] === 4)) {throw new Error("assertion failed"); }
	if (!(b[1] === 3)) {throw new Error("assertion failed"); }
	if (!(b[2] === 2)) {throw new Error("assertion failed"); }
	if (!(b[3] === 1)) {throw new Error("assertion failed"); }
	if (!(b[4] === 0)) {throw new Error("assertion failed"); }
	c = range(20);
	d = c.__getslice__(2, undefined, -1);
	if (!(d[0] === 2)) {throw new Error("assertion failed"); }
	if (!(d[1] === 1)) {throw new Error("assertion failed"); }
	if (!(d[2] === 0)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`A`	*/

A.prototype.__class__ = A;
A.__name__ = "A";
A.__bases__ = [];
A.prototype.toString =  function A_toString()
{
	return this.__$UID$__;
}/*end->	`toString`	*/

var main =  function main()
{
	var a,ok,d,err3,err2,err1,err4;
	d = [];
		if (len(d))
	{
		err1 = 1;
	}
	else
	{
		err1 = 0;
	}
		if (len([]))
	{
		err2 = 1;
	}
	else
	{
		err2 = 0;
	}
	d.append("xxx");
		if (len(d))
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
	a =  new A();
	ok = false;
		if (a !== null)
	{
		ok = true;
	}
	if (!(ok)) {throw new Error("assertion failed"); }
	a.x = [];
		if (len(a.x))
	{
		err4 = 1;
	}
	else
	{
		err4 = 0;
	}
	if (!(err4 === 0)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```
* [insert.py](list/insert.py)

input:
------
```python
from runtime import *
"""insert"""
def main():
	a = [1,2,3,4]
	assert( len(a)==4 )

	a.insert(0, 'hi')
	assert( len(a)==5 )
	assert( a[0]=='hi' )

	a.insert(1, a.pop(0))
	assert( a[0]==1 )
	assert( a[1]=='hi' )

main()
```
output:
------
```javascript


var main =  function main()
{
	var a;
	a = [1, 2, 3, 4];
	if (!(len(a) === 4)) {throw new Error("assertion failed"); }
	a.insert(0, "hi");
	if (!(len(a) === 5)) {throw new Error("assertion failed"); }
	if (!(a[0] === "hi")) {throw new Error("assertion failed"); }
	a.insert(1, __jsdict_pop(a, 0));
	if (!(a[0] === 1)) {throw new Error("assertion failed"); }
	if (!(a[1] === "hi")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	assert( len(b)==2 )
	assert( b[0]=='hi' )
	assert( b[1]=='hi' )
	print b

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,b;
	a = ["hi"];
	console.log(a);
	b = (a.__mul__(2));
	if (!(len(b) === 2)) {throw new Error("assertion failed"); }
	if (!(b[0] === "hi")) {throw new Error("assertion failed"); }
	if (!(b[1] === "hi")) {throw new Error("assertion failed"); }
	console.log(b);
}/*end->	`main`	*/

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
	a[ 2:4 ] = 'XXXY'

	#if BACKEND=='DART':
	#	print(a[...])
	#else:
	#	print(a)

	assert( a[0]==0 )
	assert( a[1]==1 )

	assert( a[2]=='X' )
	assert( a[3]=='X' )
	assert( a[4]=='X' )
	assert( a[5]=='Y' )

	assert( a[6]==4 )
	assert( a[7]==5 )
	assert( a[8]==6 )
	assert( a[9]==7 )
	assert( a[10]==8 )
	assert( a[11]==9 )

	b = list(range(3))
	c = b [ :2 ]
	assert( c[0]==0 )
	assert( c[1]==1 )

	b[ :2 ] = 'ABC'
	assert( len(b)==4 )
	assert( b[0]=='A' )

	d = list(range(10))
	d[ 2:4 ] = [99, 100]
	assert( d[0]==0 )
	assert( d[1]==1 )
	assert( d[2]==99 )
	assert( d[3]==100 )

main()
```
output:
------
```javascript


var main =  function main()
{
	var a,c,b,d;
	a = list(range(10));
	a.__setslice__(2, 4, undefined, "XXXY");
	if (!(a[0] === 0)) {throw new Error("assertion failed"); }
	if (!(a[1] === 1)) {throw new Error("assertion failed"); }
	if (!(a[2] === "X")) {throw new Error("assertion failed"); }
	if (!(a[3] === "X")) {throw new Error("assertion failed"); }
	if (!(a[4] === "X")) {throw new Error("assertion failed"); }
	if (!(a[5] === "Y")) {throw new Error("assertion failed"); }
	if (!(a[6] === 4)) {throw new Error("assertion failed"); }
	if (!(a[7] === 5)) {throw new Error("assertion failed"); }
	if (!(a[8] === 6)) {throw new Error("assertion failed"); }
	if (!(a[9] === 7)) {throw new Error("assertion failed"); }
	if (!(a[10] === 8)) {throw new Error("assertion failed"); }
	if (!(a[11] === 9)) {throw new Error("assertion failed"); }
	b = list(range(3));
	c = b.__getslice__(undefined, 2, undefined);
	if (!(c[0] === 0)) {throw new Error("assertion failed"); }
	if (!(c[1] === 1)) {throw new Error("assertion failed"); }
	b.__setslice__(undefined, 2, undefined, "ABC");
	if (!(len(b) === 4)) {throw new Error("assertion failed"); }
	if (!(b[0] === "A")) {throw new Error("assertion failed"); }
	d = list(range(10));
	d.__setslice__(2, 4, undefined, [99, 100]);
	if (!(d[0] === 0)) {throw new Error("assertion failed"); }
	if (!(d[1] === 1)) {throw new Error("assertion failed"); }
	if (!(d[2] === 99)) {throw new Error("assertion failed"); }
	if (!(d[3] === 100)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var a,idx;
	a = [1, 2, 3, 4];
	idx = 1;
	if (!(a[0] === 1)) {throw new Error("assertion failed"); }
	if (!(a[idx] === 2)) {throw new Error("assertion failed"); }
	if (!(a.index(3) === 2)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var a,y,b,z,w;
	a = [1, 2, 3];
	y = 0;
	var __iter0 = a;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var x = __iter0[ __n0 ];
		y += x;
	}
	if (!(y === 6)) {throw new Error("assertion failed"); }
	b = range(3);
	z = 0;
	var __iter0 = b;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var x = __iter0[ __n0 ];
		z += x;
	}
	if (!(z === 3)) {throw new Error("assertion failed"); }
	w = 0;
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
	var a,idx;
	a = [1, 2, 3, 4];
	idx = 1;
	if (!(a[0] === 1)) {throw new Error("assertion failed"); }
	if (!(a[idx] === 2)) {throw new Error("assertion failed"); }
	a[0] = "hello";
	a[1] = "world";
	if (!(a[0] === "hello")) {throw new Error("assertion failed"); }
	if (!(a[1] === "world")) {throw new Error("assertion failed"); }
	a.append("xxx");
	if (!(a[4] === "xxx")) {throw new Error("assertion failed"); }
	if (!(len(a) === 5)) {throw new Error("assertion failed"); }
	a.append("yyy");
	if (!(a[5] === "yyy")) {throw new Error("assertion failed"); }
	if (!(len(a) === 6)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var y,x;
	x = [100, 10, 3, 2, 1];
	__sort_method(x);
	if (!(x[0] === 1)) {throw new Error("assertion failed"); }
	if (!(x[1] === 2)) {throw new Error("assertion failed"); }
	if (!(x[2] === 3)) {throw new Error("assertion failed"); }
	if (!(x[3] === 10)) {throw new Error("assertion failed"); }
	if (!(x[4] === 100)) {throw new Error("assertion failed"); }
	y = ["C", "B", "A"];
	__sort_method(y);
	if (!(y[0] === "A")) {throw new Error("assertion failed"); }
	if (!(y[1] === "B")) {throw new Error("assertion failed"); }
	if (!(y[2] === "C")) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var a,b;
	a = ["foo", "bar"];
	if (!(__contains__(a, "foo"))) {throw new Error("assertion failed"); }
	b = [0, 1, 2];
	if (!(__contains__(b, 2))) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	b = a.pop()
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
	var a,c,b,d;
	a = list(range(10));
	b = a.pop();
	if (!(b === 9)) {throw new Error("assertion failed"); }
	c = __jsdict_pop(a, 0);
	if (!(c === 0)) {throw new Error("assertion failed"); }
	d = ["A", "B", "C"];
	if (!(__jsdict_pop(d, 1) === "B")) {throw new Error("assertion failed"); }
	if (!(len(d) === 2)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

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
	var a;
	var __comp__0;
	var idx0;
	var iter0;
	var get0;
	__comp__0 = [];
	idx0 = 0;
	iter0 = 3;
	while (idx0 < iter0)
	{
		var x;
		x = idx0;
		__comp__0.push(x);
		idx0 ++;
	}
	a = __comp__0;
	if (!(len(a) === 3)) {throw new Error("assertion failed"); }
	if (!(a[0] === 0)) {throw new Error("assertion failed"); }
	if (!(a[1] === 1)) {throw new Error("assertion failed"); }
	if (!(a[2] === 2)) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```