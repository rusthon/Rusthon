PythonJS 0.8.6
############

.. image:: http://1.bp.blogspot.com/-yG3zuA_sEM4/Uogurz5xBnI/AAAAAAAAAgk/57_Zv2iSfgo/s400/pythonjs-0.8.5.png


Introduction
======

PythonJS is a Python to Javascript translator written in
Python, created by Amirouche Boubekki and Brett Hartshorn,
currently maintained and developed by Brett. It features:
list comprehensions, classes, multiple inheritance, operator
overloading, function and class decorators, generator functions,
HTML DOM, and easily integrates with JavaScript and external JavaScript 
libraries.  The generated code works in the Browser and in NodeJS.

Speed
---------------
PythonJS allows you to select which features you need for
each section of your code, where you need performance you
can disable operator overloading, and other slow operations.
Features can be switched off and on for blocks of code using
`pythonjs.configure()` or the special `with` statements and
decorators described below.  When PythonJS is run in fast
mode (javascript with inline functions) it beats PyPy in the 
Richards, Pystone, and N-Body benchmarks.

NodeJS
---------------
Using PythonJS you can quickly port your server side code to
using NodeJS.  If you are using Tornado, porting is even
simpler because we have written a compatibility layer that
emulates the Tornado API and hides the NodeJS internal
modules.

How does it work?
----------------
Translation to JavaScript is done in two steps::

	+------------+    +-----------------+    +------------+
	¦ .py source ¦--->¦ pythonjs subset ¦--->¦ .js source ¦
	+------------+    +-----------------+    +------------+

First, the script walks the AST tree of Python source and
translates it into the subset of Python called `pythonjs`.
This reduced subset is still valid Python code, and its
AST gets parsed again in the second translation phase
that converts it into final JavaScript form.


Getting Started
===============

Get Source Code::

	git clone https://github.com/PythonJS/PythonJS.git

Translate Your Script::

	cd PythonJS/pythonjs
	./translator.py myscript1.py myscript2.py > ~/myapp.js

The translator.py script can take in multiple Python
scripts, these are appended together, and translated into a
single JavaScript.  The output is printed to stdout.  If no
command line arguments is given, then translator.py takes
input from stdin.




Writing PythonJS Scripts
=====================

Function Types
---------------

PythonJS has three main types of functions: 
	__normal__
	__fastdef__
	__javascript__

By default a function is __normal__ and fully emulates the Python standard, it allows for: arguments, keyword args with defaults, variable length arguments (*args) and variable length keyword args (**kwargs).  Functions that are __normal__ also have special logic that allows them to be called from external JavaScript like normal JavaScript functions (keyword args become normal positional arguments when called from JavaScript).  Calling __normal__ functions is slow because of this overhead, when you need faster function calls you can use __fastdef__ or __javascript__.

Functions decorated with @fastdef, or inside a __with fastdef:__ block become __fastdef__ type functions.  This makes calling them much faster, but they do not support variable length arguments (*args) or variable length keyword args (**kwargs).
Another limitation is that when called from external JavaScript you must pack args into an Array as the first argument, and pack keyword arguments into an Object as the second argument.

Functions decorated with @javascript, or inside a __with javascript:__ block, or following the call: __pythonjs.configure(javascript=True)__ become __javascript__ type functions, these offer the highest calling speed.  They do not support *args or **kwargs.  When called from external JavaScript, keyword arguments are not given by name, they become positional arguments that default to the default value if undefined.  When called from within PythonJS code, they need to be called from inside a __with javascript:__ block, or following the call pythonjs.configure(javascript=True) that sets all following code to be in __javascript__ mode.

Example::

	pythonjs.configure( javascript=True )

	def myfunc(x,y,z, a=1,b=2,c=3):
		print x,y,z,a,b,c

Example JavaScript Translation::

	myfunc = function(x, y, z, a, b, c) {
	  if (a === undefined) a = 1;
	  if (b === undefined) b = 2;
	  if (c === undefined) c = 3;
	  console.log(x, y, z, a, b, c);
	}



Generator Functions
-------------------

Functions that use the yield keyword are generator functions.  They allow you to quickly write complex iterables.
PythonJS supports simple generator functions that have a single for loop, and up to three yield statements.
The first yield comes before the for loop, and the final yield comes after the for loop.
The compiler will translate your generator function into a simple class with state-machine.  This implementation
bypasses using the native JavaScript yield keyword, and ensures that your generator function can work in all
web browsers.  

Instances of the generator function will have a next method.  Using a for loop to iterate over a generator function will automatically call its next method.

Example::

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

Example Output::

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


Directly Calling JavaScript Functions
---------------

HTML DOM Example::

	<html><head>
	<script src="pythonscript.js"></script>

	<script type="text/python">

	count = 0

	def mycallback():
		global count
		print( con.getAttribute('id') )
		btn = document.getElementById('mybutton')
		btn.firstChild.nodeValue = 'COUNTER:'+count
		count += 1

	a = 'hello'
	b = 'world'

	def test():
		con = document.createElement( 'div' )
		con.setAttribute('id', 'mydiv')
		document.body.appendChild(con)
		txt = document.createTextNode( a+b )
		con.appendChild(txt)

		window.setInterval( mycallback, 1000 )

	</script>

	</head><body>

	<button id="mybutton" onclick="test()">click me</button>

	</body>
	</html>

PythonJS allows you to call any JavaScript function directly
by wrapping it at runtime.  Attributes of JavaScript objects
are also returned directly, like document.body.  This allows
you to use the HTML DOM API just as you would in normal
JavaScript.

---------------

Inline JavaScript
---------------

There are times that JavaScript needs to be directly inlined
into PythonJS code, this is done with the special
'JS([str])' function that takes a string literal as its only
argument.  The compiler will insert the string directly into
the final output JavaScript.

JS Example::

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
The 'instanceof' function will be translated into using the
'instanceof' JavaScript operator.  At the end, arr.push is
called without wrapping it in JS(), this is allowed because
from PythonJS, we can directly call JavaScript functions by
dynamically wrapping it at runtime.

This code is more clear than before, but the downside is
that the calls to arr.push will be slower because it gets
wrapped at runtime.  To have fast and clear code we need to
use the final method below, 'with javascript'

2. with javascript::

	with javascript:
		arr = []
		ob = {}
		if instanceof(arr, Array):
			arr.push('hello world')
			arr.push( ob )

The "with javascript:" statement can be used to mark a block
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

Example::

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
care of wrapping the method for you so that "self" is bound
to the method, and is callable from JavaScript.

Example::

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
can do this now simply by passing the instance.  This only
works with property getter/setters.

Example::

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
prototypes from PythonJS using some special syntax.

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
functions must be defined inside a "with javascript:" block,
and the decorator format is:
`[class name].prototype.[function name]`


---------------

Making PythonJS Wrappers for JavaScript Libraries
------------------------------

The above techniques provide all the tools you will need to
interact with JavaScript code, and easily write wrapper code
in PythonJS.  The last tool you will need, is a standard way
of creating JavaScript objects, storing a reference to the
instance, and later passing the instance to wrapped
JavaScript function.  In JavaScript objects are created with
the `new` keyword, in PythonJS you can use the `new()`
function instead.  To store an instance created by `new()`,
you should assign it to `self` like this:
`self[...] = new( SomeJavaScriptClass() )`.

If you have never seen `...` syntax in Python it is the
rarely used Ellipsis syntax, we have hijacked it in PythonJS
as a special case to assign something to a hidden attribute.
The builtin types: tuple, list, dict, etc, are wrappers that
internally use JavaScript Arrays or Objects, to get to these
internal objects you use the Ellipsis syntax.  The following
example shows how the THREE.js binding wraps the Vector3
object and combines operator overloading.

Example::

	class Vector3:
		def __init__(self, x=0, y=0, z=0, object=None ):
			if object:
				self[...] = object
			else:
				with javascript:
					self[...] = new(THREE.Vector3(x,y,z))

		@property
		def x(self):
			with javascript: return self[...].x
		@x.setter
		def x(self, value):
			with javascript: self[...].x = value

		@property
		def y(self):
			with javascript: return self[...].y
		@y.setter
		def y(self, value):
			with javascript: self[...].y = value

		@property
		def z(self):
			with javascript: return self[...].z
		@z.setter
		def z(self, value):
			with javascript: self[...].z = value

		def set(self, x,y,z):
			self[...].set(x,y,z)

		def add(self, other):
			assert isinstance(other, Vector3)
			self.set( self.x+other.x, self.y+other.y, self.z+other.z )
			return self

		def addScalar(self, s):
			self.set( self.x+s, self.y+s, self.z+s )
			return self

		def __add__(self, other):
			if instanceof(other, Object):
				assert isinstance(other, Vector3)
				return Vector3( self.x+other.x, self.y+other.y, self.z+other.z )
			else:
				return Vector3( self.x+other, self.y+other, self.z+other )

		def __iadd__(self, other):
			if instanceof(other, Object):
				self.add( other )
			else:
				self.addScalar( other )


---------------

Optimized Function Calls
------------------------------

By default PythonJS functions have runtime call checking
that ensures you have called the function with the required
number of arguments, and also checks to see if you had
called the function from JavaScript - and if so adapt the
arguments.  This adds some overhead each time the function
is called, and will generally be about 15 times slower than
normal Python.  When performance is a concern you can
decorate functions that need to be fast with @fastdef, or
use the `with fastdef:` with statement.  Note that functions
that do not have arguments are always fast.  Using fastdef
will make each call to your function 100 times faster, so if
you call the same function many times in a loop, it is a
good idea to decorate it with @fastdef.

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
@javascript decorator, or nest the function inside a `with
javascript:` statement.

Example::

	@javascript
	def f( a,b,c, x=1, y=2, z=3 ):
		return a+b+c+x+y+z

	// javascript
	f( 1,2,3, 100, 200, 300 );



---------------

NodeJS
======

PythonJS can also be used to write server side software
using NodeJS.  You can use the nodejs.py helper script to
translate your python script and run it in NodeJS.  This has
been tested with NodeJS v0.10.22.

Example::

	cd PythonJS
	./nodejs.py myscript.py

The directory PythonJS/nodejs/bindings contains wrappers for
using NodeJS modules.  Some of these wrappers emulate parts
of Pythons standard library, like: os, sys, io, and
subprocess.  The example below imports the fake io and sys
libraries, and prints the contents of a file passed as the
last command line argument to nodejs.py.

Example::

	from nodejs.io import *
	from nodejs.sys import *

	path = sys.argv[ len(sys.argv)-1 ]
	f = open( path, 'rb' )
	print f.read()

------------------------------


Test Server
===========

PythonJS includes two test servers that run the HTML tests
in PythonJS/tests.  Both of these servers are written using
the Tornado API.  The NodeJS version is a port of the
original test server adapted to work with the Tornado
compatible binding.


NodeJS Tornado
---------------

Install Modules::

	sudo npm install -g mime
	sudo npm install -g ws

Run NodeJS Server::

	cd PythonJS
	./nodejs.py nodejs/tests/tornado-demo-server.py


Python Tornado
---------------

Install Tornado for Python3::

	wget https://pypi.python.org/packages/source/t/tornado/tornado-3.1.1.tar.gz
	tar xvf tornado-3.1.1.tar.gz
	cd tornado-3.1.1
	python3 setup.py build
	sudo python3 setup.py install

Run Python Server::

	cd PythonJS/tests
	./server.py

Testing
-------

After running one of the test servers above, open a web
browser and go to: http://localhost:8080

The test server dynamically compiles Python into JavaScript,
this greatly speeds up the testing and development process.
Any html file you place in the PythonJS/tests directory will
become available as a new web-page.  When this web-page is
requested the server will parse the html and check all the
<script> tags for external or embedded Python, and
dynamically convert it to JavaScript.

External Python Scripts::

	<head>
	<script src="bindings/three.py"></script>
	</head>

The server knows that the above script needs to be
dynamically compiled to JavaScript because the script is
located in the "bindings" directory and the file name ends
with ".py"

Embedded Python Scripts::

	<body>
	<script type="text/python">
	from three import *
	v1 = Vector3( x=1, y=2, z=3 )
	v2 = Vector3( x=4, y=5, z=6 )
	v3 = v1 + v2
	</script>
	</body>

The server knows that above is an embedded Python script
because the script tag has its type attribute set to
"text/python".  The server will compile and replace the
Python code with JavaScript, change the type attribute to be
"text/javascript", and serve the page to the client.

The syntax "from three import *" tells the compiler to load
static type information about the previously compiled
binding "three.py" into the compilers namespace, this is
required because three.py uses operator overloading to wrap
the THREE.js API.  PythonJS programs are explicitly and
implicitly statically typed to allow for operator
overloading and optimizations.


.. image:: https://d2weczhvl823v0.cloudfront.net/PythonJS/pythonjs/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

