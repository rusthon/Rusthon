requires
-------
https://github.com/rusthon/Rusthon/blob/master/pythonjs/pythonjs-minimal.js
https://github.com/rusthon/Rusthon/blob/master/pythonjs/pythonjs.js

You need one of the above, pythonjs.js is complete and 58K, less pythonic
code might be able to get by with just including pythonjs-minimal.js thats only 14K.

Classes
-----------
```python
	class A:
		def __init__(self, x,y,z):
			self.x = x
			self.y = y
			self.z = z

		def foo(self, w):
			return self.x + w

```

javascript
----------
```javascript
	A = function(x, y, z) {
	  A.__init__(this, x,y,z);
	}

	A.prototype.__init__ = function(x, y, z) {
	  this.x=x;
	  this.y=y;
	  this.z=z;
	}
	A.__init__ = function () { return A.prototype.__init__.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };

	A.prototype.foo = function(w) {
	  return (this.x + w);
	}
	A.foo = function () { return A.prototype.foo.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };
```

Method Overrides
----------------
In the example above, you might be wondering why in the JavaScript translation, is the class A constructor calling `A.__init__(this, x,y,z)`, and why is the `__init__` method assigned `A.prototype` and then wrapped and assigned to `A.__init__`.  This is done so that subclasses are able to override their parent's methods, but still have a way of calling them, an example that subclasses A will make this more clear.

```python
	class B( A ):
		def __init__(self, w):
			A.__init__(self, 10, 20, 30)
			self.w = w
```

javascript
----------
```javascript
	B = function(w) {
	  B.__init__(this, w);
	}

	B.prototype.__init__ = function(w) {
	  A.__init__(this,10,20,30);
	  this.w=w;
	}
	B.__init__ = function () { return B.prototype.__init__.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };

	for (var n in A.prototype) {  if (!(n in B.prototype)) {    B.prototype[n] = A.prototype[n]  }};
```

The above output Javascript shows how the constructor for `B` calls `B.__init__` which then calls `B.prototype.__init__`.
`B.prototype.__init__` calls `A.__init__` passing `this` as the first argument.  This emulates in JavaScript how unbound methods work in Python.  When using the Dart backend, the output is different but the concept is the same - static "class methods" are created that implement the method body, the instance methods are just short stubs that call the static "class methods".


Generator Functions
-------------------

Functions that use the `yield` keyword are generator functions.  They allow you to quickly write complex iterables.
PythonJS supports simple generator functions that have a single for loop, and up to three `yield` statements.
The first `yield` comes before the for loop, and the final `yield` comes after the for loop.
The compiler will translate your generator function into a simple class with state-machine.  This implementation
bypasses using the native JavaScript `yield` keyword, and ensures that your generator function can work in all web browsers.  

Instances of the generator function will have a next method.  Using a for loop to iterate over a generator function will automatically call its next method.

```python
	def fib(n):
		yield 'hello'
		a, b = 0, 1
		for x in range(n):
			yield a
			a,b = b, a+b
		yield 'world'

	def test():
		for n in fib(20):
			print n
```

javascript
--------
```javascript
	fib = function(n) {
	  this.n = n;
	  this.__head_yield = "hello";
	  this.__head_returned = 0;
	  var __r_0;
	  __r_0 = [0, 1];
	  this.a = __r_0[0];
	  this.b = __r_0[1];
	  this.__iter_start = 0;
	  this.__iter_index = 0;
	  this.__iter_end = this.n;
	  this.__done__ = 0;
	}

	fib.prototype.next = function() {
	  if (( this.__head_returned ) == 0) {
	    this.__head_returned = 1;
	    return this.__head_yield;
	  } else {
	    if (( this.__iter_index ) < this.__iter_end) {
	      __yield_return__ = this.a;
	      var __r_1;
	      __r_1 = [this.b, (this.a + this.b)];
	      this.a = __r_1[0];
	      this.b = __r_1[1];
	      this.__iter_index += 1
	      return __yield_return__;
	    } else {
	      this.__done__ = 1;
	      __yield_return__ = "world";
	      return __yield_return__;
	    }
	  }
	}

	test = function(args, kwargs) {
	  var __iterator__, n;
	  var n, __generator__;
	  __generator__ = new fib(20);
	  while(( __generator__.__done__ ) != 1) {
	    n = __generator__.next();
	    console.log(n);
	  }
	}
```

Inline JavaScript
---------------

There are times that JavaScript needs to be directly inlined
into PythonJS code, this is done with the special
`JS([str])` function that takes a string literal as its only
argument.  The compiler will insert the string directly into
the final output JavaScript.

####JS Example

	JS("var arr = new Array()")
	JS("var ob = new Object()")
	JS("ob['key'] = 'value'")
	if JS("Object.prototype.toString.call( arr ) === '[object Array]'"):
		JS("arr.push('hello world')")
		JS("arr.push( ob )")

In the example above we create a new JavaScript Array.
Notice that the if-statement above has a condition that is
inlined JavaScript.
