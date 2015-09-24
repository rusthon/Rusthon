JavaScript Backend Regression Tests - dict
-----------------------------
the following tests compiled, and run in nodejs without any errors
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
/***/ if (f.__recompile !== undefined) { eval("f.__redef="+f.__recompile); f.__recompile=undefined; };
/***/ if (f.__redef !== undefined) { return f.__redef.apply(this,arguments); };
	
	/*pass*/
}/*end->	`f`	*/

var G =  function G()
{
/***/ if (G.__recompile !== undefined) { eval("G.__redef="+G.__recompile); G.__recompile=undefined; };
/***/ if (G.__redef !== undefined) { return G.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`G`	*/

G.prototype.__class__ = G;
G.__name__ = "G";
G.__bases__ = [];
G.prototype.toString =  function G_toString()
{
/***/ if (G_toString.__recompile !== undefined) { eval("G_toString.__redef="+G_toString.__recompile); G_toString.__recompile=undefined; };
/***/ if (G_toString.__redef !== undefined) { return G_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
var __$UID$__=0;
var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
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
		if (__comp__0.__setitem__) { __comp__0.__setitem__(a, "xxx") }
		else { __comp__0[a] = "xxx" }
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var err3,err2,err1,d;
	d = dict({  }, { copy:false });
	if (__jsdict_keys(d).length instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (__jsdict_keys(d).length)
	{
		err1 = 1;
	}
	else
	{
		err1 = 0;
	}
	if (len(__jsdict_keys(dict({  }, { copy:false }))) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
	if (len(__jsdict_keys(dict({  }, { copy:false }))))
	{
		err2 = 1;
	}
	else
	{
		err2 = 0;
	}
	if (d.__setitem__) { d.__setitem__("x", "xxx") }
	else { d["x"] = "xxx" }
	if (len(__jsdict_keys(d)) instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
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
"""dict.keys() and iter"""

def main():
	a = {'foo':'bar'}
	keys = a.keys()
	assert( 'foo' in keys )

	print 'testing iter over dict'
	## this is not allowed, a must be wrapped with `iter(a)`
	#for key in a:
	print a
	for key in iter(a):
		print key
		print a[key]

main()
```
output:
------
```javascript


var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,keys;
	a = dict({  }, { copy:false, keytype:"string", iterable:[["foo", "bar"]] });
	keys = __jsdict_keys(a);
	if (!(__contains__(keys, "foo"))) {throw new Error("assertion failed"); }
	console.log("testing iter over dict");
	console.log(a);
	var __iter0 = a;
	if (! (__iter0 instanceof Array || typeof __iter0 == "string" || __is_typed_array(__iter0) || __is_some_array(__iter0) )) { __iter0 = __object_keys__(__iter0) }
	for (var __n0 = 0; __n0 < __iter0.length; __n0++) {
		var key = __iter0[ __n0 ];
		console.log(key);
		console.log(a[key]);
	}
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
/***/ if (f.__recompile !== undefined) { eval("f.__redef="+f.__recompile); f.__recompile=undefined; };
/***/ if (f.__redef !== undefined) { return f.__redef.apply(this,arguments); };
	
	/*pass*/
}/*end->	`f`	*/

var G =  function G()
{
/***/ if (G.__recompile !== undefined) { eval("G.__redef="+G.__recompile); G.__recompile=undefined; };
/***/ if (G.__redef !== undefined) { return G.__redef.apply(this,arguments); };
	this.__$UID$__ = __$UID$__ ++;
}/*end->	`G`	*/

G.prototype.__class__ = G;
G.__name__ = "G";
G.__bases__ = [];
G.prototype.toString =  function G_toString()
{
/***/ if (G_toString.__recompile !== undefined) { eval("G_toString.__redef="+G_toString.__recompile); G_toString.__recompile=undefined; };
/***/ if (G_toString.__redef !== undefined) { return G_toString.__redef.apply(this,arguments); };
	return this.__$UID$__;
}/*end->	`toString`	*/

G.prototype.get =  function G_get(x, _kwargs_)
{
/***/ if (G_get.__recompile !== undefined) { eval("G_get.__redef="+G_get.__recompile); G_get.__recompile=undefined; };
/***/ if (G_get.__redef !== undefined) { return G_get.__redef.apply(this,arguments); };
	
	var y = (_kwargs_===undefined || (typeof(_kwargs_)=='object' && _kwargs_.y===undefined))?	null :   typeof(_kwargs_)=='object'?_kwargs_.y: __invalid_call__('function `get` requires named keyword arguments, invalid parameter for `y`',arguments);
	if (y instanceof Array) {throw new RuntimeError("if test not allowed directly on arrays. The correct syntax is: `if len(array)` or `if array.length`")}
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
/***/ if (G_set.__recompile !== undefined) { eval("G_set.__redef="+G_set.__recompile); G_set.__recompile=undefined; };
/***/ if (G_set.__redef !== undefined) { return G_set.__redef.apply(this,arguments); };
	
	console.log("set method ok");
	console.log([x, y]);
	return true;
}/*end->	`set`	*/

G.prototype.items =  function G_items()
{
/***/ if (G_items.__recompile !== undefined) { eval("G_items.__redef="+G_items.__recompile); G_items.__recompile=undefined; };
/***/ if (G_items.__redef !== undefined) { return G_items.__redef.apply(this,arguments); };
	
	return true;
}/*end->	`items`	*/

G.prototype.pop =  function G_pop(x)
{
/***/ if (G_pop.__recompile !== undefined) { eval("G_pop.__redef="+G_pop.__recompile); G_pop.__recompile=undefined; };
/***/ if (G_pop.__redef !== undefined) { return G_pop.__redef.apply(this,arguments); };
	
	return x;
}/*end->	`pop`	*/

var main =  function main()
{
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a,newkeys,g,i,o,p,u,v;
	g =  new G();
	a = dict({  }, { copy:false, keytype:"int", iterable:[[2, 22], [3, 33]] });
	if (!(a[2] === 22)) {throw new Error("assertion failed"); }
	if (!(a[3] === 33)) {throw new Error("assertion failed"); }
	console.log(__jsdict_get(a, 1, "getok"));
	if (!(__jsdict_get(a, "none", "default") === "default")) {throw new Error("assertion failed"); }
	if (!(__jsdict_get(g, 1) === 1)) {throw new Error("assertion failed"); }
	if (!(g.get(0, { y:2 }) === 2)) {throw new Error("assertion failed"); }
	/***/ try {
	__jsdict_set(a, 0, "hi");
	/***/ } catch (__err) { if (__debugger__.onerror(__err, main, __jsdict_set)==true){debugger;}else{throw __err;} };
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
/***/ if (main.__recompile !== undefined) { eval("main.__redef="+main.__recompile); main.__recompile=undefined; };
/***/ if (main.__redef !== undefined) { return main.__redef.apply(this,arguments); };
	var a;
	a = dict({  }, { copy:false, keytype:"int", iterable:[[2, 22], [3, 33]] });
	if (!(__contains__(a, 2))) {throw new Error("assertion failed"); }
	if (!(__contains__(a, 3))) {throw new Error("assertion failed"); }
}/*end->	`main`	*/

main();
```