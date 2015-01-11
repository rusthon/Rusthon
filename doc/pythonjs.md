
Python vs JavaScript Modes
-------------------------

PythonJS has two primary modes you can write code in: `python` and `javascript`.  The default mode is `python`, you can mark sections of your code to use either mode with `pythonjs.configure(javascript=True/False)` or nesting blocks inside `with python:` or `with javascript:`.  The `javascript` mode can be used for sections of code where performance is a major concern.  When in `javascript` mode Python dictionaries become JavaScript Objects.  In both modes you can directly call external JavaScript functions, its only faster in `javascript` mode because function calls are direct without any wrapping.


Function Types
---------------

PythonJS has three main types of functions: `normal`, `fastdef`, and `javascript`.

By default a function is "normal" and fully emulates the Python standard, it allows for: arguments, keyword args with defaults, variable length arguments (*args) and variable length keyword args (**kwargs).  Functions that are "normal" also have special logic that allows them to be called from external JavaScript like normal JavaScript functions (keyword args become normal positional arguments when called from JavaScript).  Calling "normal" functions is slow because of this overhead, when you need faster function calls you can use "fastdef" or "javascript".

Functions decorated with `@fastdef`, or inside a `with fastdef:` block become "fastdef" type functions.  This makes calling them faster, but they do not support variable length arguments (*args) or variable length keyword args (**kwargs).
Another limitation is that when called from external JavaScript you must pack args into an Array as the first argument, and pack keyword arguments into an Object as the second argument.

Functions decorated with @javascript, or inside a `with javascript:` block, or following the call: `pythonjs.configure(javascript=True)` become `javascript` type functions, these offer the highest calling speed.  They do not support *args or **kwargs.  When called from external JavaScript, keyword arguments are not given by name, they become positional arguments that default to the default value if undefined.  When called from within PythonJS code, they need to be called from inside a `with javascript:` block, or following the call `pythonjs.configure(javascript=True)` that sets all following code to be in `javascript` mode.

####Example

	pythonjs.configure( javascript=True )

	def myfunc(x,y,z, a=1,b=2,c=3):
		print x,y,z,a,b,c

####Example JavaScript Translation

	myfunc = function(x, y, z, a, b, c) {
	  if (a === undefined) a = 1;
	  if (b === undefined) b = 2;
	  if (c === undefined) c = 3;
	  console.log(x, y, z, a, b, c);
	}

Class Types
-----------

PythonJS has two types of classes: `normal` and `javascript`.  By default classes are `normal` and support operator overloading and properties.  Calling methods on a `javascript` class is much faster than method calls on a `normal` class, but follow the same rules as described above for `javascript` type functions.  Both class types can be used from external JavaScript, the only difference is that instances of a "normal" class can pass their methods directly as arguments to a function that will use the method as a callback - even if that external function depends on the context of `this`.  Whereas instances of a `javascript` class can not directly pass their methods as arguments, because they depend on the calling context of `this` - if you are familiar with JavaScript this comes as no surprise.

Example::

	pythonjs.configure( javascript=True )
	class A:
		def __init__(self, x,y,z):
			self.x = x
			self.y = y
			self.z = z

		def foo(self, w):
			return self.x + w

Example JavaScript Translation::

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


Method Overrides
----------------
In the example above, you might be wondering why in the JavaScript translation, is the class A constructor calling `A.__init__(this, x,y,z)`, and why is the `__init__` method assigned `A.prototype` and then wrapped and assigned to `A.__init__`.  This is done so that subclasses are able to override their parent's methods, but still have a way of calling them, an example that subclasses A will make this more clear.

####Example

	class B( A ):
		def __init__(self, w):
			A.__init__(self, 10, 20, 30)
			self.w = w

####Example JavaScript Translation

	B = function(w) {
	  B.__init__(this, w);
	}

	B.prototype.__init__ = function(w) {
	  A.__init__(this,10,20,30);
	  this.w=w;
	}
	B.__init__ = function () { return B.prototype.__init__.apply(arguments[0], Array.prototype.slice.call(arguments,1)) };

	for (var n in A.prototype) {  if (!(n in B.prototype)) {    B.prototype[n] = A.prototype[n]  }};


The above output Javascript shows how the constructor for `B` calls `B.__init__` which then calls `B.prototype.__init__`.
`B.prototype.__init__` calls `A.__init__` passing `this` as the first argument.  This emulates in JavaScript how unbound methods work in Python.  When using the Dart backend, the output is different but the concept is the same - static "class methods" are created that implement the method body, the instance methods are just short stubs that call the static "class methods".

####Example Dart Translation

	class B implements A {
	  var y;
	  var x;
	  var z;
	  var w;
	  B(w) {B.__init__(this,w);}
	  static void __init__(self, w) {
	    A.__init__(self,10,20,30);
	    self.w=w;
	  }

	  foo(w) { return A.__foo(this,w); }
	}

Above the method `foo` calls the static class method `A.__foo`.  Note that the static class methods are automatically prefixed with `__`.


Multiple Inheritance
--------------------

Multiple inheritance is fully supported for both JavaScript and Dart backends.  When using the Dart backend it will generate stub-methods that call static class methods that are prefixed with `__`.
Methods that the subclass extends can call: ParentClassName.some_method(self) and this will be translated into: ParentClassName.__some_method(this)

#### Example

	class A:
		def foo(self):
			print 'foo'

	class B:
		def bar(self):
			print 'bar'

	class C( A, B ):
		def call_foo_bar(self):
			print 'call_foo_bar in subclass C'
			self.foo()
			self.bar()

		## extend foo ##
		def foo(self):
			A.foo(self)
			print 'foo extended'

#### Example Dart Translation

	class A {
	  foo() { return A.__foo(this); }
	  static __foo(self) {
	    print("foo");
	  }

	}
	class B {
	  bar() { return B.__bar(this); }
	  static __bar(self) {
	    print("bar");
	  }

	}
	class C implements A, B {
	  call_foo_bar() { return C.__call_foo_bar(this); }
	  static __call_foo_bar(self) {
	    print("call_foo_bar in subclass C");
	    self.foo();
	    self.bar();
	  }

	  foo() { return C.__foo(this); }
	  static __foo(self) {
	    A.__foo(self);
	    print("foo extended");
	  }

	  bar() { return B.__bar(this); }
	}


Generator Functions
-------------------

Functions that use the `yield` keyword are generator functions.  They allow you to quickly write complex iterables.
PythonJS supports simple generator functions that have a single for loop, and up to three `yield` statements.
The first `yield` comes before the for loop, and the final `yield` comes after the for loop.
The compiler will translate your generator function into a simple class with state-machine.  This implementation
bypasses using the native JavaScript `yield` keyword, and ensures that your generator function can work in all web browsers.  

Instances of the generator function will have a next method.  Using a for loop to iterate over a generator function will automatically call its next method.

####Example

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

####Example Output

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


---------------

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
inlined JavaScript.  Lets take a look at two alternative
ways this can be rewritten.

1. JSArray, JSObject, and instanceof::

	arr = JSArray()
	ob = JSObject()
	if instanceof(arr, Array):
		arr.push('hello world')
		arr.push( ob )

The special function JSArray will create a new JavaScript
Array object, and JSObject creates a new JavaScript Object.
The `instanceof` function will be translated into using the
'instanceof' JavaScript operator.  At the end, arr.push is
called without wrapping it in `JS()`, this is allowed because
from PythonJS, we can directly call JavaScript functions by
dynamically wrapping it at runtime.

This code is more clear than before, but the downside is
that the calls to arr.push will be slower because it gets
wrapped at runtime.  To have fast and clear code we need to
use the final method below, `with javascript`

2. with javascript::

	with javascript:
		arr = []
		ob = {}
		if instanceof(arr, Array):
			arr.push('hello world')
			arr.push( ob )

The `with javascript:` statement can be used to mark a block
of code as being direct JavaScript.  The compiler will
basically wrap each line it can in JS() calls.  The calls to
arr.push will be fast because there is no longer any runtime
wrapping.  Instead of using JSArray and JSObject you just
use the literal notation to create them.

---------------

Calling PythonJS Functions from JavaScript
------------------------------

PythonJS functions can be used as callbacks in Javascript
code, there are no special calling conventions that you need
to worry about.  Simply define a function in PythonJS and
call it from JavaScript.  Note that if your PythonJS
function uses keyword arguments, you can use them as a
normal positional arguments.

####Example

	# PythonJS
	def my_pyfunction( a,b,c, optional='some default'):
		print a,b,c, optional

	// javascript
	my_pyfunction( 1,2,3, 'my kwarg' );


---------------

Calling PythonJS Methods from JavaScript
------------------------------

Calling PythonJS methods is also simple, you just need to
create an instance of the class in PythonJS and then pass
the method to a JavaScript function, or assign it to a new
variable that the JavaScript code will use.  PythonJS takes
care of wrapping the method for you so that `self` is bound
to the method, and is callable from JavaScript.

####Example

	// javascript
	function js_call_method( method_callback ) {
		method_callback( 1,2,3 )
	}

	# PythonJS
	class A:
		def my_method(self, a,b,c):
			print self, a,b,c
			self.a = a
			self.b = b
			self.c = c

	a = A()
	js_call_method( a.my_method )


---------------

Passing PythonJS Instances to JavaScript
------------------------------

If you are doing something complex like deep integration
with an external JavaScript library, the above technique of
passing each method callback to JavaScript might become
inefficient.  If you want to pass the PythonJS instance
itself and have its methods callable from JavaScript, you
can do this now simply by passing the instance.

####Example

	// javascript
	function js_function( pyob ) {
		pyob.foo( 1,2,3 )
		pyob.bar( 4,5,6 )
	}

	# PythonJS
	class A:
		def foo(self, a,b,c):
			print a+b+c
		def bar(self, a,b,c):
			print a*b*c

	a = A()
	js_function( a )


---------------

Define JavaScript Prototypes from PythonJS
------------------------------

If you are going beyond simple integration with an external
JavaScript library, and perhaps want to change the way it
works on a deeper level, you can modify JavaScript
prototypes from PythonJS using some special syntax that will
set the function on the prototype as an non-enumerable property.

Example::

	with javascript:

		@String.prototype.upper
		def func():
			return this.toUpperCase()

		@String.prototype.lower
		def func():
			return this.toLowerCase()

		@String.prototype.index
		def func(a):
			return this.indexOf(a)

The above example shows how we modify the String type in
JavaScript to act more like a Python string type.  The
functions must be defined inside a `with javascript:` block,
and the decorator format is:
`[class name].prototype.[function name]`


Optimized Function Calls
------------------------------

By default PythonJS functions have runtime call checking
that ensures you have called the function with the required
number of arguments, and also checks to see if you had
called the function from JavaScript - and if so adapt the
arguments.  This adds some overhead each time the function
is called, and will generally be about 15 times slower than
normal Python.  When performance is a concern you can
decorate functions that need to be fast with `@fastdef`, or
use the `with fastdef:` with statement.  Note that functions
that do not have arguments are always fast.  Using fastdef
will make each call to your function 100 times faster, so if
you call the same function many times in a loop, it is a
good idea to decorate it with `@fastdef`.

Example::

	@fastdef
	def f1( a, b, c ):
		return a+b+c

	with fastdef:
		def f2( a,b,c, x=1,y=2,z=3):
			return a+b+c+x+y+z

If you need to call a fastdef function from JavaScript you
will need to call it with arguments packed into an array as
the first argument, and keyword args packed into an Object
as the second argument.

Example::

	// javascript
	f2( [1,2,3], {x:100, y:200, z:300} );

If you need fast function that is callable from javascript
without packing its arguments like above, you can use the
`@javascript` decorator, or nest the function inside a `with
javascript:` statement.

Example::

	@javascript
	def f( a,b,c, x=1, y=2, z=3 ):
		return a+b+c+x+y+z

	// javascript
	f( 1,2,3, 100, 200, 300 );

